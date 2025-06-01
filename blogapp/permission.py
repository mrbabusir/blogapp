from rest_framework import permissions

class IsAuthorOrReadonly(permissions.BasePermission): #custome permmsion authorley matrai edit garna pauney post/comments

    def has_object_permission(self,request, view, obj):
        if request.method in permissions.SAFE_METHODS: ##read permission banako for anyone who requesting
            return True
        
        return obj.user == request.user