"""
User service
"""
from app.models.user import User
from app.database import db
from app.utils.security import hash_password, verify_password

class UserService:
    """Handle user profile operations"""
    
    def get_user_profile(self, user_id: int) -> dict:
        """
        Get user profile including salt for key derivation
        
        Args:
            user_id: User ID
            
        Returns:
            dict: User profile data
            
        Raises:
            ValueError: If user not found
        """
        user = User.query.get(user_id)
        if not user:
            raise ValueError('User not found')
        
        return user.to_dict(include_salt=True)
    
    def update_user_profile(self, user_id: int, name: str) -> bool:
        """
        Update user profile (name)
        
        Args:
            user_id: User ID
            name: New name
            
        Returns:
            bool: Success status
            
        Raises:
            ValueError: If user not found
        """
        user = User.query.get(user_id)
        if not user:
            raise ValueError('User not found')
        
        user.name = name
        db.session.commit()
        
        return True
    
    def change_password(self, user_id: int, old_password: str, new_password: str) -> bool:
        """
        Change user password
        
        Args:
            user_id: User ID
            old_password: Current password
            new_password: New password
            
        Returns:
            bool: Success status
            
        Raises:
            ValueError: If verification fails
        """
        user = User.query.get(user_id)
        if not user:
            raise ValueError('User not found')
        
        # Verify old password
        if not verify_password(old_password, user.password_hash):
            raise ValueError('Invalid old password')
        
        # Hash and update new password
        user.password_hash = hash_password(new_password)
        db.session.commit()
        
        return True
