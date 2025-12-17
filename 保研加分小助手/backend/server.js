// server.js - 主服务器文件
const express = require('express');
const cors = require('cors');
const MockDatabase = require('./mockData');

const app = express();
const port = 3000;

// 初始化模拟数据库
const db = new MockDatabase();

// 中间件
app.use(cors());
app.use(express.json());

// 登录API接口
app.post('/api/login', (req, res) => {
    console.log('收到登录请求:', req.body);
    
    const { username, password } = req.body;

    // 验证参数
    if (!username || !password) {
        return res.json({
            success: false,
            message: '账号和密码不能为空'
        });
    }

    // 验证账号长度
    if (username.length !== 15) {
        return res.json({
            success: false,
            message: '账号长度必须为15位'
        });
    }

    // 验证密码长度
    if (password.length > 20) {
        return res.json({
            success: false,
            message: '密码长度不能超过20位'
        });
    }

    // 验证登录信息
    const result = db.validateLogin(username, password);
    console.log('登录结果:', result);
    
    res.json(result);
});

// 启动服务器
app.listen(port, () => {
    console.log('=== 服务器启动成功 ===');
    console.log(`服务器地址: http://localhost:${port}`);
    console.log('登录API: POST http://localhost:3000/api/login');
    console.log('测试账号: 202300000000001 / 123456');
    console.log('========================');
});