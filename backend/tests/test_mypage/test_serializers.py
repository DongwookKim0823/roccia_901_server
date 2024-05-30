from unittest.mock import MagicMock

from account.models import User
from mypage.serializers import (
    LevelCountSerializer,
    MypageSerializer,
    UserProfileSerializer,
)


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


class TestLevelCountSerializer:

    def test_level_count_serializer_serialization(self):
        data = {"workout_level": 1, "total_count": 10}
        serializer = LevelCountSerializer(data)
        assert serializer.data == {"workout_level": "하얀색", "total_count": 10}


class TestMypageSerializer:

    def test_mypage_serializer(self, mock_boulder_problem_object, mock_record_object, mock_user_model):
        mock_boulder_problem_object.return_value.values.return_value.annotate.return_value.order_by.return_value = [
            {"workout_level": 1, "total_count": 10},
            {"workout_level": 2, "total_count": 20},
        ]
        mock_record_object.return_value.annotate.return_value.aggregate.return_value = {
            "total": MagicMock(total_seconds=MagicMock(return_value=330 * 60))
        }
        serializer = MypageSerializer(instance=mock_user_model)
        data = serializer.data

        expected_data = {
            "profile": {
                "username": mock_user_model.username,
                "generation": mock_user_model.generation,
                "role": mock_user_model.role,
                "workout_location": mock_user_model.workout_location,
                "workout_level": dict(User.WORKOUT_LEVELS)[mock_user_model.workout_level],
                "profile_number": mock_user_model.profile_number,
                "introduction": mock_user_model.introduction,
            },
            "total_workout_time": 330,
            "records": [
                {"workout_level": "하얀색", "total_count": 10},
                {"workout_level": "노란색", "total_count": 20},
            ],
        }

        assert data == expected_data
