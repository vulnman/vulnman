from rest_framework import mixins


class AgentCreateModelMixin(mixins.CreateModelMixin):
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user, project=self.request.auth.project)


class AgentListModelMixin(mixins.ListModelMixin):
    pass


class AgentDestroyModelMixin(mixins.DestroyModelMixin):
    pass


class AgentRetrieveModelMixin(mixins.RetrieveModelMixin):
    pass


class AgentUpdateModelMixin(mixins.UpdateModelMixin):
    pass
