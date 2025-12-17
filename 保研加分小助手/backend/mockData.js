// mockData.js - 模拟数据库
class MockDatabase {
    constructor() {
        // 模拟用户表
        this.users = [
            {
                id: 1,
                username: '202300000000001',
                password: '123456',
                role: 'student',
                name: '张三'
            },
            {
                id: 2,
                username: '202300000000002',
                password: 'abcdef',
                role: 'student',
                name: '李四'
            }
        ];
    }

    // 根据用户名查找用户
    findUserByUsername(username) {
        return this.users.find(user => user.username === username);
    }

    // 验证用户登录
    validateLogin(username, password) {
        const user = this.findUserByUsername(username);
        if (!user) {
            return { success: false, message: '用户不存在' };
        }
        
        if (user.password !== password) {
            return { success: false, message: '密码错误' };
        }
        
        return { 
            success: true, 
            message: '登录成功',
            user: {
                id: user.id,
                username: user.username,
                name: user.name,
                role: user.role
            }
        };
    }
}

module.exports = MockDatabase;