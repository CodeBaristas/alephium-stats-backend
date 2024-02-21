# NOTE:actual no db necessary
# from sqlmodel.ext.asyncio.session import AsyncSession
# from sqlmodel.sql.expression import Select, SelectOfScalar
#
# from .rating.crud import PerformedUserRatingsCRUD, RatingCRUD
#
# SelectOfScalar.inherit_cache = True
# Select.inherit_cache = True
# AsyncSession.not_autoflush = True
# AsyncSession.not_autoflush = True
#
#
# class CRUD(AsyncSession):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#         # RATNG
#         self.rating = RatingCRUD(self)
#         self.performed_user_ratings = PerformedUserRatingsCRUD(self)
