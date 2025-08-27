# app/models/mixins.py
class ToDictMixin:
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
