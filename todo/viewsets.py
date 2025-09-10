from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from todo.models import Todo
from todo.serializers import TodoSerializer, TodoReorderSerializer, TodoCreateSerializer, TodoCompleteSerializer


class TodoViewSet(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Todo.objects.all()

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TodoSerializer
        elif self.action in ('create', 'update', 'partial_update'):
            return TodoCreateSerializer
        elif self.action == 'reorder':
            return TodoReorderSerializer
        elif self.action == 'complete':
            return TodoCompleteSerializer
        return TodoSerializer

    def get_queryset(self):
        qs = Todo.objects.filter(user=self.request.user).order_by('position')
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['patch'])
    def reorder(self, request: Request, pk: int=None):
        serializer = TodoReorderSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        new_position = serializer.data['position']
        todo = self.get_object()

        try:
            todo.reorder(new_position)
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def complete(self, request: Request, pk: int=None):
        serializer = TodoCompleteSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        completed = serializer.data['completed']
        todo = self.get_object()

        # block request if already completed
        if completed and todo.completed:
            return Response({'message': 'This todo task is already completed.'}, status=status.HTTP_400_BAD_REQUEST)
        # complete and send email
        elif completed and not todo.completed:
            try:
                todo.complete()
            except Exception:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # clear completion flag
        elif not completed and todo.completed:
            todo.completed = False
            todo.save(update_fields='completed')

        return Response(serializer.data, status=status.HTTP_200_OK)