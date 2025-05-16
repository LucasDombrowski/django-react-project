from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Match
# Correct the import path for PointsAttributionHelper
from .services.points_attribution_helper import PointsAttributionHelper 

@receiver(post_save, sender=Match)
def attribute_points_on_match_finish(sender, instance, created, update_fields, **kwargs):
    """
    Listens for a Match instance to be saved. If the match is marked as finished,
    it processes bets and attributes points.
    """
    # We are interested in the moment is_finished becomes True.
    # 'created' is False means it's an update.
    # 'update_fields' tells us which fields were updated. If it's None, all fields might have been.
    
    was_finished_field_updated = update_fields is not None and 'is_finished' in update_fields
    
    # If it's a new instance and created as finished, or if is_finished was just updated to True
    if instance.is_finished and (created or was_finished_field_updated):
        # Check a flag on the instance to prevent re-entry if process_match_bets_and_attribute_points itself saves the match
        # Though in our current helper, it only saves User objects.
        if hasattr(instance, '_points_attributed_already') and instance._points_attributed_already:
            return

        print(f"Match {instance.id} finished. Triggering points attribution.")
        helper = PointsAttributionHelper(match_instance=instance)
        result = helper.process_match_bets_and_attribute_points()
        print(f"Points attribution result for Match {instance.id}: {result}")
        
        # Set a flag to prevent re-entry in the same save cycle if other saves happen
        # This might be overly cautious depending on exact flow, but safe.
        instance._points_attributed_already = True
    elif not instance.is_finished and was_finished_field_updated:
        # If is_finished was changed from True to False, we might want to reset a flag if we used one.
        if hasattr(instance, '_points_attributed_already'):
            del instance._points_attributed_already 