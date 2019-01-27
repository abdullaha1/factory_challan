from django.contrib.auth.models import User

from master_data.models.company import Company
from master_data.models.user_profile import UserProfile


class RegisterController():
    """
    creating user and company
    """
    def create_user(register_form):
        user = User.objects.create(
            first_name=register_form['first_name'],
            last_name=register_form['last_name'],
            email=register_form['email'],
            username=register_form['email']
        )
        user.set_password(register_form['password'])
        user.save()

        company = Company.objects.create(
            name=register_form['company_name'],
            company_url=register_form['company_url'],
            status="Trial",
            created_by_id=user.id,
            updated_by_id=user.id,
        )

        UserProfile.objects.create(
            user=user,
            company=company,
            middle_name=register_form['middle_name']
        )
