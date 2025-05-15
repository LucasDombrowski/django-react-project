import os
from PIL import Image
from django.core.exceptions import ValidationError

class CustomImageValidator:
    MAX_IMAGE_UPLOAD_SIZE_MB = 2
    MAX_IMAGE_UPLOAD_SIZE_BYTES = MAX_IMAGE_UPLOAD_SIZE_MB * 1024 * 1024
    ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png']
    MAX_IMAGE_WIDTH = 1024
    MAX_IMAGE_HEIGHT = 1024

    @staticmethod
    def validate(image_file_obj, field_name_for_error_message):
        if not image_file_obj: # Field is optional and not provided
            return

        # File size validation
        if image_file_obj.size > CustomImageValidator.MAX_IMAGE_UPLOAD_SIZE_BYTES:
            raise ValidationError(
                f"{field_name_for_error_message}: Image file too large. Maximum size is {CustomImageValidator.MAX_IMAGE_UPLOAD_SIZE_MB}MB."
            )

        # File extension validation
        ext = os.path.splitext(image_file_obj.name)[1].lower()
        if ext not in CustomImageValidator.ALLOWED_IMAGE_EXTENSIONS:
            raise ValidationError(
                f"{field_name_for_error_message}: Invalid image format. Allowed formats are {', '.join(CustomImageValidator.ALLOWED_IMAGE_EXTENSIONS)}."
            )

        # Dimension and actual format validation using Pillow
        try:
            image_file_obj.seek(0) 
            img = Image.open(image_file_obj)
            img.verify()
            
            image_file_obj.seek(0)
            img = Image.open(image_file_obj)

            actual_format = img.format.lower()
            is_allowed_format = False
            if actual_format == 'jpeg' and ('.jpg' in CustomImageValidator.ALLOWED_IMAGE_EXTENSIONS or '.jpeg' in CustomImageValidator.ALLOWED_IMAGE_EXTENSIONS):
                is_allowed_format = True
            elif actual_format in [fmt.replace('.', '') for fmt in CustomImageValidator.ALLOWED_IMAGE_EXTENSIONS]:
                is_allowed_format = True
            
            if not is_allowed_format:
                raise ValidationError(
                    f"{field_name_for_error_message}: Invalid image content or format. Allowed types: {', '.join(CustomImageValidator.ALLOWED_IMAGE_EXTENSIONS)}."
                )

            if img.width > CustomImageValidator.MAX_IMAGE_WIDTH or img.height > CustomImageValidator.MAX_IMAGE_HEIGHT:
                raise ValidationError(
                    f"{field_name_for_error_message}: Image dimensions too large. Maximum dimensions are {CustomImageValidator.MAX_IMAGE_WIDTH}x{CustomImageValidator.MAX_IMAGE_HEIGHT} pixels."
                )
        except FileNotFoundError:
            raise ValidationError(f"{field_name_for_error_message}: Image file not found.")
        except Exception as e:
            raise ValidationError(f"{field_name_for_error_message}: Invalid image file. Could not be processed. Error: {e}") 