from flask import Blueprint
from .controllers import 

produto_bp = Blueprint('produto', __name__)

produto_bp.route('/produto', methods=['POST'])(  )