from flask import Flask, jsonify, request
from datetime import datetime
import uuid

app = Flask(__name__)

# ข้อมูลจำลองสำหรับ testing
users = [
    {"id": 1, "name": "John Doe", "email": "john@example.com"},
    {"id": 2, "name": "Jane Smith", "email": "jane@example.com"},
    {"id": 3, "name": "Bob Johnson", "email": "bob@example.com"}
]

products = [
    {"id": 1, "name": "Laptop", "price": 999.99, "category": "Electronics"},
    {"id": 2, "name": "Mouse", "price": 29.99, "category": "Electronics"},
    {"id": 3, "name": "Keyboard", "price": 59.99, "category": "Electronics"}
]

@app.route('/')
def home():
    """หน้าแรกของ API"""
    return jsonify({
        "message": "Welcome to Testing API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "GET /": "หน้าแรก",
            "GET /health": "ตรวจสอบสถานะ API",
            "GET /users": "ดึงข้อมูลผู้ใช้ทั้งหมด",
            "GET /users/<id>": "ดึงข้อมูลผู้ใช้ตาม ID",
            "POST /users": "เพิ่มผู้ใช้ใหม่",
            "GET /products": "ดึงข้อมูลสินค้าทั้งหมด",
            "GET /products/<id>": "ดึงข้อมูลสินค้าตาม ID",
            "POST /products": "เพิ่มสินค้าใหม่"
        }
    })

@app.route('/health')
def health_check():
    """ตรวจสอบสถานะของ API"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "uptime": "running"
    })

# User endpoints
@app.route('/users', methods=['GET'])
def get_users():
    """ดึงข้อมูลผู้ใช้ทั้งหมด"""
    return jsonify({
        "success": True,
        "data": users,
        "count": len(users)
    })
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """ดึงข้อมูลผู้ใช้ตาม ID"""
    user = next((user for user in users if user["id"] == user_id), None)
    if user:
        return jsonify({
            "success": True,
            "data": user
        })
    else:
        return jsonify({
            "success": False,
            "message": "ไม่พบผู้ใช้"
        }), 404

@app.route('/users', methods=['POST'])
def create_user():
    """เพิ่มผู้ใช้ใหม่"""
    data = request.get_json()
    
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({
            "success": False,
            "message": "กรุณาระบุ name และ email"
        }), 400
    
    new_user = {
        "id": len(users) + 1,
        "name": data["name"],
        "email": data["email"]
    }
    
    users.append(new_user)
    
    return jsonify({
        "success": True,
        "message": "เพิ่มผู้ใช้สำเร็จ",
        "data": new_user
    }), 201

# Product endpoints
@app.route('/products', methods=['GET'])
def get_products():
    """ดึงข้อมูลสินค้าทั้งหมด"""
    return jsonify({
        "success": True,
        "data": products,
        "count": len(products)
    })

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """ดึงข้อมูลสินค้าตาม ID"""
    product = next((product for product in products if product["id"] == product_id), None)
    if product:
        return jsonify({
            "success": True,
            "data": product
        })
    else:
        return jsonify({
            "success": False,
            "message": "ไม่พบสินค้า"
        }), 404

@app.route('/products', methods=['POST'])
def create_product():
    """เพิ่มสินค้าใหม่"""
    data = request.get_json()
    
    if not data or 'name' not in data or 'price' not in data:
        return jsonify({
            "success": False,
            "message": "กรุณาระบุ name และ price"
        }), 400
    
    new_product = {
        "id": len(products) + 1,
        "name": data["name"],
        "price": float(data["price"]),
        "category": data.get("category", "General")
    }
    
    products.append(new_product)
    
    return jsonify({
        "success": True,
        "message": "เพิ่มสินค้าสำเร็จ",
        "data": new_product
    }), 201

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "message": "ไม่พบ endpoint ที่ต้องการ"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "success": False,
        "message": "เกิดข้อผิดพลาดภายในเซิร์ฟเวอร์"
    }), 500

if __name__ == '__main__':
    print("🚀 Starting Testing API Server...")
    print("📝 Available endpoints:")
    print("   GET  / - หน้าแรก")
    print("   GET  /health - ตรวจสอบสถานะ")
    print("   GET  /users - ดึงข้อมูลผู้ใช้ทั้งหมด")
    print("   GET  /users/<id> - ดึงข้อมูลผู้ใช้ตาม ID")
    print("   POST /users - เพิ่มผู้ใช้ใหม่")
    print("   GET  /products - ดึงข้อมูลสินค้าทั้งหมด")
    print("   GET  /products/<id> - ดึงข้อมูลสินค้าตาม ID")
    print("   POST /products - เพิ่มสินค้าใหม่")
    print("\n🌐 Server running at: http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
