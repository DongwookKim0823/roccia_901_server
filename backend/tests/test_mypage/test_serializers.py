from account.models import User
from mypage.serializers import UserProfileSerializer


class TestUserProfileSerializer:
    def test_user_retrieve_serializer(self, mock_user_model):
        serializer = UserProfileSerializer(instance=mock_user_model)
        expected_data = {
            "username": mock_user_model.username,
            "generation": mock_user_model.generation,
            "role": mock_user_model.role,
            "workout_location": mock_user_model.workout_location,
            "workout_level": dict(User.WORKOUT_LEVELS)[mock_user_model.workout_level],
            "profile_number": mock_user_model.profile_number,
            "introduction": mock_user_model.introduction,
        }

        assert serializer.data == expected_data
        assert serializer.data.keys() == expected_data.keys()
