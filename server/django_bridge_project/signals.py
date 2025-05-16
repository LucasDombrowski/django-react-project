from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Match
# Correct the import path for PointsAttributionHelper
from .services.points_attribution_helper import PointsAttributionHelper 

@receiver(post_save, sender=Match)
def attribute_points_on_match_finish(sender, instance, created, update_fields, **kwargs):
    """
    Listens for a Match instance to be saved. If the match is marked as finished
    AND points have not yet been calculated, it processes bets and attributes points.
    Ensures this runs only when is_finished transitions to True or on creation as finished.
    """
    
    process_points = False
    if instance.is_finished and not instance.points_calculation_done:
        if created: # Case 1: Newly created and already finished.
            process_points = True
        elif not created: # Case 2: Updated.
            if update_fields is None: # Full save, and is_finished is True. Assume it could be the trigger.
                process_points = True
            elif 'is_finished' in update_fields: # Specifically updated to is_finished = True.
                process_points = True

    if process_points:
        print(f"Match {instance.id} is finished and points not calculated. Triggering points attribution. Created: {created}, Update_fields: {update_fields}")
        helper = PointsAttributionHelper(match_instance=instance)
        result = helper.process_match_bets_and_attribute_points()
        print(f"Points attribution result for Match {instance.id}: {result}")
        
        if result.get("status") == "success" or result.get("status") == "info":
            instance.points_calculation_done = True
            instance.save(update_fields=['points_calculation_done'])
            print(f"Match {instance.id} marked as points_calculation_done=True.")
    
    # Logic to reset points_calculation_done if match is reverted to not finished
    elif not instance.is_finished and instance.points_calculation_done:
        reset_flag = False
        if not created: # Only apply to updates
            if update_fields is None: # Full save, and is_finished is False now.
                reset_flag = True
            elif 'is_finished' in update_fields: # Specifically updated to is_finished = False.
                reset_flag = True
        
        if reset_flag:
            print(f"Match {instance.id} was marked as not finished, resetting points_calculation_done flag. Update_fields: {update_fields}")
            instance.points_calculation_done = False
            instance.save(update_fields=['points_calculation_done']) 