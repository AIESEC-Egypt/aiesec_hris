from .authentication_views import (
    LoginView,
    LogoutView,
    ChangePasswordView,
    ResetPasswordView,
    ForgotPasswordView)
from .experience_points_views import ExperiencePointsUpdate
from .index_view import IndexView
from .lc_views import LCList, LCDetail
from .message_view import MessageView
from .moderation_views import reviews_list, profile_accept, profile_decline
from .position_views import positions_json
from .profile_decline_update_view import ProfileDeclineUpdate
from .profile_views import (
    ProfileDetail,
    ProfileUpdate)
from .register_view import RegisterView
from .stats_views import StatsView
