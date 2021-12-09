
class IgnoreFieldsAfterCreationMixin(object):
    ignore_fields_after_creation = None

    def get_ignore_fields_after_creation(self):
        if not self.ignore_fields_after_creation:
            return []
        return self.ignore_fields_after_creation

    def update(self, request, *args, **kwargs):
        request.data._mutable = True
        for field in self.get_ignore_fields_after_creation():
            if request.data.get(field):
                request.data.pop(field)
        request.data._mutable = False
        return super().update(request, *args, **kwargs)
