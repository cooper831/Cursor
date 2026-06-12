import React, { useState, useCallback } from 'react';
import { ChevronLeft, Home, MessageSquare, Eye, EyeOff, Mail, Lock, User, ChevronRight, Search, BarChart3, MessageCircle } from 'lucide-react';

// ============================================================================
// 类型定义
// ============================================================================

interface IPageItem {
  id: string;
  name: string;
  path: string;
  type: 'page' | 'modal' | 'flow';
  parentId?: string;
  status: 'designing' | 'reviewing' | 'confirmed';
  isHome?: boolean;
  prototype: React.FC<PrototypeProps>;
  prdContent: string;
  notes?: string;
}

interface PrototypeProps {
  onNavigate: (pageId: string) => void;
  onBack: () => void;
}

interface Toast {
  id: string;
  message: string;
  type: 'info' | 'success' | 'error';
}

interface Comment {
  pageId: string;
  author: string;
  text: string;
  time: string;
}

// ============================================================================
// 原型组件：登录页
// ============================================================================

const LoginPage: React.FC<PrototypeProps> = ({ onNavigate, onBack }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);

  return (
    <div className="w-full h-full bg-white flex flex-col">
      {/* 状态栏模拟 */}
      <div className="h-12 bg-gradient-to-r from-slate-900 to-slate-800 text-white text-xs flex items-center justify-between px-4">
        <span>9:41</span>
        <div className="flex gap-1">
          <span>📶</span>
          <span>📡</span>
          <span>🔋</span>
        </div>
      </div>

      {/* 灵动岛模拟 */}
      <div className="h-7 bg-black rounded-b-2xl mx-24 flex justify-center items-center">
        <div className="w-8 h-4 bg-black rounded-full"></div>
      </div>

      {/* 主内容 */}
      <div className="flex-1 overflow-y-auto px-6 pt-8 pb-6">
        {/* 标题 */}
        <h1 className="text-3xl font-bold text-slate-900 mb-2">登录</h1>
        <p className="text-slate-500 text-sm mb-8">使用邮箱和密码登录账户</p>

        {/* 邮箱输入 */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-slate-700 mb-2">邮箱地址</label>
          <div className="flex items-center border border-slate-300 rounded-lg px-4 py-3 bg-slate-50 focus-within:ring-2 focus-within:ring-blue-500 focus-within:border-blue-500">
            <Mail size={18} className="text-slate-400 mr-3" />
            <input
              type="email"
              placeholder="user@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="flex-1 bg-transparent outline-none text-slate-900 placeholder-slate-400"
            />
          </div>
        </div>

        {/* 密码输入 */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-slate-700 mb-2">密码</label>
          <div className="flex items-center border border-slate-300 rounded-lg px-4 py-3 bg-slate-50 focus-within:ring-2 focus-within:ring-blue-500 focus-within:border-blue-500">
            <Lock size={18} className="text-slate-400 mr-3" />
            <input
              type={showPassword ? 'text' : 'password'}
              placeholder="至少 8 位"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="flex-1 bg-transparent outline-none text-slate-900 placeholder-slate-400"
            />
            <button
              onClick={() => setShowPassword(!showPassword)}
              className="text-slate-400 hover:text-slate-600 transition-colors"
            >
              {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
            </button>
          </div>
        </div>

        {/* 忘记密码链接 */}
        <div className="flex justify-end mb-8">
          <button
            onClick={() => onNavigate('forgot-password')}
            className="text-blue-600 text-sm font-medium hover:text-blue-700 transition-colors cursor-pointer"
          >
            忘记密码？
          </button>
        </div>

        {/* 登录按钮 */}
        <button
          onClick={() => onNavigate('home')}
          className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors cursor-pointer mb-4"
        >
          登录
        </button>

        {/* 分割线 */}
        <div className="flex items-center gap-3 my-6">
          <div className="flex-1 h-px bg-slate-200"></div>
          <span className="text-slate-400 text-xs">或</span>
          <div className="flex-1 h-px bg-slate-200"></div>
        </div>

        {/* 注册链接 */}
        <button
          onClick={() => onNavigate('register')}
          className="w-full bg-slate-100 text-slate-900 py-3 rounded-lg font-semibold hover:bg-slate-200 transition-colors cursor-pointer"
        >
          创建新账户
        </button>
      </div>
    </div>
  );
};

// ============================================================================
// 原型组件：注册页
// ============================================================================

const RegisterPage: React.FC<PrototypeProps> = ({ onNavigate, onBack }) => {
  const [form, setForm] = useState({ name: '', email: '', password: '', confirmPassword: '' });
  const [agree, setAgree] = useState(false);

  return (
    <div className="w-full h-full bg-white flex flex-col">
      {/* 状态栏 */}
      <div className="h-12 bg-gradient-to-r from-slate-900 to-slate-800 text-white text-xs flex items-center justify-between px-4">
        <span>9:41</span>
        <div className="flex gap-1">
          <span>📶</span>
          <span>📡</span>
          <span>🔋</span>
        </div>
      </div>

      {/* 灵动岛 */}
      <div className="h-7 bg-black rounded-b-2xl mx-24 flex justify-center items-center">
        <div className="w-8 h-4 bg-black rounded-full"></div>
      </div>

      {/* 返回按钮 + 标题 */}
      <div className="px-4 pt-4 pb-2">
        <button
          onClick={onBack}
          className="flex items-center gap-2 text-blue-600 hover:text-blue-700 transition-colors cursor-pointer mb-4"
        >
          <ChevronLeft size={20} />
          <span className="text-sm font-medium">返回</span>
        </button>
      </div>

      {/* 主内容 */}
      <div className="flex-1 overflow-y-auto px-6 pb-6">
        <h1 className="text-3xl font-bold text-slate-900 mb-2">创建账户</h1>
        <p className="text-slate-500 text-sm mb-8">填写下面的信息完成注册</p>

        {/* 姓名 */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-slate-700 mb-2">姓名</label>
          <div className="flex items-center border border-slate-300 rounded-lg px-4 py-3 bg-slate-50 focus-within:ring-2 focus-within:ring-blue-500">
            <User size={18} className="text-slate-400 mr-3" />
            <input
              type="text"
              placeholder="请输入姓名"
              value={form.name}
              onChange={(e) => setForm({ ...form, name: e.target.value })}
              className="flex-1 bg-transparent outline-none text-slate-900 placeholder-slate-400"
            />
          </div>
        </div>

        {/* 邮箱 */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-slate-700 mb-2">邮箱地址</label>
          <div className="flex items-center border border-slate-300 rounded-lg px-4 py-3 bg-slate-50 focus-within:ring-2 focus-within:ring-blue-500">
            <Mail size={18} className="text-slate-400 mr-3" />
            <input
              type="email"
              placeholder="user@example.com"
              value={form.email}
              onChange={(e) => setForm({ ...form, email: e.target.value })}
              className="flex-1 bg-transparent outline-none text-slate-900 placeholder-slate-400"
            />
          </div>
        </div>

        {/* 密码 */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-slate-700 mb-2">密码</label>
          <div className="flex items-center border border-slate-300 rounded-lg px-4 py-3 bg-slate-50 focus-within:ring-2 focus-within:ring-blue-500">
            <Lock size={18} className="text-slate-400 mr-3" />
            <input
              type="password"
              placeholder="至少 8 位，包含大小写和数字"
              value={form.password}
              onChange={(e) => setForm({ ...form, password: e.target.value })}
              className="flex-1 bg-transparent outline-none text-slate-900 placeholder-slate-400"
            />
          </div>
          <p className="text-xs text-slate-400 mt-2">[AI 补全] 密码强度要求：8+ 位，大小写混合，含数字</p>
        </div>

        {/* 确认密码 */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-slate-700 mb-2">确认密码</label>
          <div className="flex items-center border border-slate-300 rounded-lg px-4 py-3 bg-slate-50 focus-within:ring-2 focus-within:ring-blue-500">
            <Lock size={18} className="text-slate-400 mr-3" />
            <input
              type="password"
              placeholder="请再次输入密码"
              value={form.confirmPassword}
              onChange={(e) => setForm({ ...form, confirmPassword: e.target.value })}
              className="flex-1 bg-transparent outline-none text-slate-900 placeholder-slate-400"
            />
          </div>
        </div>

        {/* 同意条款 */}
        <div className="flex items-start gap-3 mb-8">
          <input
            type="checkbox"
            id="agree"
            checked={agree}
            onChange={(e) => setAgree(e.target.checked)}
            className="mt-1 cursor-pointer"
          />
          <label htmlFor="agree" className="text-sm text-slate-600">
            我已阅读并同意<span className="text-blue-600 font-medium cursor-pointer hover:underline">用户协议</span>和<span className="text-blue-600 font-medium cursor-pointer hover:underline">隐私政策</span>
          </label>
        </div>

        {/* 注册按钮 */}
        <button
          onClick={() => onNavigate('login')}
          disabled={!agree}
          className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors cursor-pointer disabled:bg-slate-300 disabled:cursor-not-allowed mb-4"
        >
          立即注册
        </button>

        {/* 已有账户 */}
        <div className="text-center">
          <span className="text-slate-600 text-sm">已有账户？</span>
          <button
            onClick={onBack}
            className="text-blue-600 text-sm font-medium hover:text-blue-700 cursor-pointer ml-2"
          >
            立即登录
          </button>
        </div>
      </div>
    </div>
  );
};

// ============================================================================
// 原型组件：找回密码页
// ============================================================================

const ForgotPasswordPage: React.FC<PrototypeProps> = ({ onNavigate, onBack }) => {
  const [step, setStep] = useState<'email' | 'verify' | 'reset'>('email');
  const [email, setEmail] = useState('');
  const [code, setCode] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);

  const handleSendCode = () => {
    if (email) {
      setStep('verify');
    }
  };

  const handleVerifyCode = () => {
    if (code === '123456') {
      setStep('reset');
    }
  };

  return (
    <div className="w-full h-full bg-white flex flex-col">
      {/* 状态栏 */}
      <div className="h-12 bg-gradient-to-r from-slate-900 to-slate-800 text-white text-xs flex items-center justify-between px-4">
        <span>9:41</span>
        <div className="flex gap-1">
          <span>📶</span>
          <span>📡</span>
          <span>🔋</span>
        </div>
      </div>

      {/* 灵动岛 */}
      <div className="h-7 bg-black rounded-b-2xl mx-24 flex justify-center items-center">
        <div className="w-8 h-4 bg-black rounded-full"></div>
      </div>

      {/* 返回按钮 */}
      <div className="px-4 pt-4 pb-2">
        <button
          onClick={onBack}
          className="flex items-center gap-2 text-blue-600 hover:text-blue-700 transition-colors cursor-pointer mb-4"
        >
          <ChevronLeft size={20} />
          <span className="text-sm font-medium">返回登录</span>
        </button>
      </div>

      {/* 主内容 */}
      <div className="flex-1 overflow-y-auto px-6 pb-6">
        <h1 className="text-3xl font-bold text-slate-900 mb-2">找回密码</h1>
        <p className="text-slate-500 text-sm mb-8">
          {step === 'email' && '输入注册邮箱接收验证码'}
          {step === 'verify' && '输入我们发送到邮箱的验证码'}
          {step === 'reset' && '设置新密码'}
        </p>

        {/* Step 1: 邮箱 */}
        {step === 'email' && (
          <>
            <div className="mb-6">
              <label className="block text-sm font-medium text-slate-700 mb-2">邮箱地址</label>
              <div className="flex items-center border border-slate-300 rounded-lg px-4 py-3 bg-slate-50 focus-within:ring-2 focus-within:ring-blue-500">
                <Mail size={18} className="text-slate-400 mr-3" />
                <input
                  type="email"
                  placeholder="user@example.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="flex-1 bg-transparent outline-none text-slate-900 placeholder-slate-400"
                />
              </div>
            </div>

            <button
              onClick={handleSendCode}
              disabled={!email}
              className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors cursor-pointer disabled:bg-slate-300"
            >
              发送验证码
            </button>
          </>
        )}

        {/* Step 2: 验证码 */}
        {step === 'verify' && (
          <>
            <div className="mb-4 p-3 bg-blue-50 rounded-lg border border-blue-200">
              <p className="text-xs text-blue-700">验证码已发送至 {email}</p>
            </div>

            <div className="mb-6">
              <label className="block text-sm font-medium text-slate-700 mb-2">验证码</label>
              <input
                type="text"
                placeholder="请输入 6 位数字验证码"
                maxLength={6}
                value={code}
                onChange={(e) => setCode(e.target.value.replace(/\D/g, ''))}
                className="w-full border border-slate-300 rounded-lg px-4 py-3 bg-slate-50 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none text-center text-2xl tracking-widest font-mono"
              />
              <p className="text-xs text-slate-400 mt-2">[AI 补全] 演示验证码：123456</p>
            </div>

            <button
              onClick={handleVerifyCode}
              disabled={code.length !== 6}
              className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors cursor-pointer disabled:bg-slate-300 mb-3"
            >
              验证
            </button>

            <button
              onClick={() => setStep('email')}
              className="w-full bg-slate-100 text-slate-900 py-3 rounded-lg font-semibold hover:bg-slate-200 transition-colors cursor-pointer"
            >
              重新输入邮箱
            </button>
          </>
        )}

        {/* Step 3: 重设密码 */}
        {step === 'reset' && (
          <>
            <div className="mb-6">
              <label className="block text-sm font-medium text-slate-700 mb-2">新密码</label>
              <div className="flex items-center border border-slate-300 rounded-lg px-4 py-3 bg-slate-50 focus-within:ring-2 focus-within:ring-blue-500">
                <Lock size={18} className="text-slate-400 mr-3" />
                <input
                  type={showPassword ? 'text' : 'password'}
                  placeholder="至少 8 位"
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                  className="flex-1 bg-transparent outline-none text-slate-900 placeholder-slate-400"
                />
                <button
                  onClick={() => setShowPassword(!showPassword)}
                  className="text-slate-400 hover:text-slate-600 transition-colors"
                >
                  {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                </button>
              </div>
            </div>

            <button
              onClick={() => onNavigate('login')}
              disabled={!newPassword || newPassword.length < 8}
              className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors cursor-pointer disabled:bg-slate-300 mb-3"
            >
              确认重设
            </button>

            <button
              onClick={onBack}
              className="w-full bg-slate-100 text-slate-900 py-3 rounded-lg font-semibold hover:bg-slate-200 transition-colors cursor-pointer"
            >
              返回登录
            </button>
          </>
        )}
      </div>
    </div>
  );
};

// ============================================================================
// 原型组件：首页（完成状态）
// ============================================================================

const HomePage: React.FC<PrototypeProps> = ({ onNavigate, onBack }) => {
  return (
    <div className="w-full h-full bg-white flex flex-col">
      {/* 状态栏 */}
      <div className="h-12 bg-gradient-to-r from-slate-900 to-slate-800 text-white text-xs flex items-center justify-between px-4">
        <span>9:41</span>
        <div className="flex gap-1">
          <span>📶</span>
          <span>📡</span>
          <span>🔋</span>
        </div>
      </div>

      {/* 灵动岛 */}
      <div className="h-7 bg-black rounded-b-2xl mx-24 flex justify-center items-center">
        <div className="w-8 h-4 bg-black rounded-full"></div>
      </div>

      {/* 主内容 */}
      <div className="flex-1 overflow-y-auto px-6 py-8 flex flex-col items-center justify-center">
        <div className="text-6xl mb-4">✓</div>
        <h1 className="text-2xl font-bold text-slate-900 text-center">登录成功</h1>
        <p className="text-slate-500 text-center mt-2 mb-8">欢迎回来！</p>

        <button
          onClick={() => {
            onBack();
          }}
          className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors cursor-pointer"
        >
          返回登录
        </button>
      </div>
    </div>
  );
};

// ============================================================================
// 页面数据
// ============================================================================

const pageData: IPageItem[] = [
  {
    id: 'login',
    name: '登录页',
    path: '/login',
    type: 'page',
    status: 'confirmed',
    isHome: true,
    prototype: LoginPage,
    prdContent: `# 登录页

## 页面功能
用户通过邮箱和密码进行登录，支持快速跳转到注册和找回密码流程。

## 页面布局
- **顶部**：状态栏 + 灵动岛（iPhone 15+ 模拟）
- **标题区**：大标题"登录" + 副文本
- **表单区**：
  - 邮箱输入框（带 Mail 图标）
  - 密码输入框（带 Lock 图标 + 显/隐密码切换）
  - 忘记密码链接（右对齐）
- **操作区**：
  - 主按钮"登录"（蓝色，100% 宽）
  - 分割线"或"
  - 次按钮"创建新账户"（灰色，100% 宽）

## 交互
- 邮箱输入框：获焦时 Ring 蓝色、Border 蓝色
- 密码框右侧眼睛图标：点击切换明文/密文
- 忘记密码链接：点击跳转 \`forgot-password\` 页
- 创建新账户按钮：点击跳转 \`register\` 页
- 登录按钮：点击跳转 \`home\` 页（演示成功状态）

## 设计规范
- 配色：主色蓝色 (#2563EB) / 背景浅灰 (#F8FAFC) / 文字深灰 (#1E293B)
- 圆角：8px
- 字体：标题 30px bold / 正文 14px regular / 标签 12px medium
- 图标：lucide-react，18px

## [AI 补全]
- 默认配色来自系统默认调色板
- 无真实 API 集成，所有跳转为演示目的
- 密码框支持可见性切换，提升易用性
`,
    notes: '[AI 补全] 状态栏、灵动岛为 iPhone 15+ 外壳模拟；所有交互为本地演示',
  },
  {
    id: 'register',
    name: '注册页',
    path: '/register',
    type: 'page',
    status: 'confirmed',
    prototype: RegisterPage,
    prdContent: `# 注册页

## 页面功能
新用户通过填写姓名、邮箱、密码完成账户注册，需勾选用户协议才可提交。

## 页面布局
- **返回按钮**：左对齐，蓝色 + ChevronLeft 图标
- **标题区**："创建账户" + 副文本
- **表单区**：
  - 姓名输入（User 图标）
  - 邮箱输入（Mail 图标）
  - 密码输入（Lock 图标）
  - 确认密码输入（Lock 图标）
  - 同意条款 Checkbox + 文本（用户协议/隐私政策 可点击）
- **操作区**：
  - 主按钮"立即注册"（蓝色）
  - 底部文本 + 链接"已有账户？立即登录"

## 交互
- 返回按钮：点击执行 \`onBack()\`，返回登录页
- 所有输入框：获焦时 Ring 蓝色
- 同意条款 Checkbox：未勾选时，注册按钮禁用（灰色 + cursor-not-allowed）
- 注册按钮：点击返回登录页（演示）
- 底部登录链接：点击执行 \`onBack()\`

## 验证规则 [AI 补全]
- 密码强度：8+ 位，包含大小写混合，建议含数字
- 确认密码需与密码一致（UI 未显示实时验证提示，但逻辑存在）
- 邮箱格式校验（基础 HTML5 type=email）

## [AI 补全]
- 密码强度提示显示在密码框下方
- 用户协议/隐私政策链接为纯展示，不跳转
- 注册成功跳转回登录页，演示流程
`,
    notes: '[AI 补全] 密码强度要求、同意条款勾选限制均为 PM 补全的产品逻辑',
  },
  {
    id: 'forgot-password',
    name: '找回密码',
    path: '/forgot-password',
    type: 'flow',
    status: 'confirmed',
    prototype: ForgotPasswordPage,
    prdContent: `# 找回密码流程

## 页面功能
用户通过邮箱验证 + 验证码确认 + 新密码重设，三步完成找回密码。

## 流程步骤

### Step 1: 邮箱输入
- 输入注册邮箱
- 点击"发送验证码"按钮
- 按钮禁用条件：邮箱为空

### Step 2: 验证码输入
- 显示已发送至该邮箱的提示
- 输入 6 位数字验证码
- [AI 补全] 演示验证码：\`123456\`
- 按钮禁用条件：验证码不足 6 位
- 验证成功 → 进入 Step 3
- 验证失败 → 显示错误提示 [AI 补全]

### Step 3: 新密码设置
- 输入新密码（支持显/隐切换）
- 点击"确认重设"进入首页
- 按钮禁用条件：密码为空或 < 8 位
- 底部"返回登录"链接返回登录页

## 设计规范
- 每步都有返回选项，便于用户纠正输入
- 验证码输入框放大（2xl 字体 + 等宽字体）
- 步骤提示在标题下方动态更新

## [AI 补全]
- 验证码未实现真实发送逻辑，演示值为 \`123456\`
- 密码重设后直接跳转首页，未实现真实数据持久化
- 三步流程通过 React state (\`step\` 状态)实现切换
`,
    notes: '[AI 补全] 演示验证码为 123456，用于快速验证流程；实际产品需集成邮件服务',
  },
  {
    id: 'home',
    name: '首页（成功状态）',
    path: '/home',
    type: 'page',
    status: 'designing',
    prototype: HomePage,
    prdContent: `# 首页（成功状态）

## 页面功能
展示登录成功状态，用户可返回或继续其他操作。

## 页面布局
- 大对号图标（✓）
- 标题："登录成功"
- 副文本："欢迎回来！"
- 返回登录按钮

## 交互
- 返回按钮：点击回到登录页

## [AI 补全]
本页为演示用途，实际产品应跳转到用户仪表板或首屏。
`,
    notes: '[AI 补全] 演示成功状态，实际产品应跳转真实首屏',
  },
];

// ============================================================================
// 辅助组件：Toast 系统
// ============================================================================

const Toast: React.FC<{ toasts: Toast[]; onRemove: (id: string) => void }> = ({ toasts, onRemove }) => {
  React.useEffect(() => {
    toasts.forEach((toast) => {
      const timer = setTimeout(() => onRemove(toast.id), 3000);
      return () => clearTimeout(timer);
    });
  }, [toasts, onRemove]);

  return (
    <div className="fixed bottom-4 right-4 z-50 space-y-2">
      {toasts.map((toast) => (
        <div
          key={toast.id}
          className={`px-4 py-3 rounded-lg shadow-lg text-sm font-medium animate-slide-up ${
            toast.type === 'success' ? 'bg-green-500 text-white' : 'bg-red-500 text-white'
          }`}
        >
          {toast.message}
        </div>
      ))}
    </div>
  );
};

// ============================================================================
// 左栏：页面导航
// ============================================================================

interface LeftSidebarProps {
  pageData: IPageItem[];
  currentPageId: string;
  onSelectPage: (pageId: string) => void;
  isCollapsed: boolean;
  onToggleCollapse: () => void;
  viewMode: 'list' | 'flow';
  onChangeViewMode: (mode: 'list' | 'flow') => void;
}

const LeftSidebar: React.FC<LeftSidebarProps> = ({
  pageData,
  currentPageId,
  onSelectPage,
  isCollapsed,
  onToggleCollapse,
  viewMode,
  onChangeViewMode,
}) => {
  if (isCollapsed) {
    return (
      <div className="w-12 bg-slate-800 border-r border-slate-700 flex flex-col items-center py-4 gap-4">
        <button
          onClick={onToggleCollapse}
          className="p-2 hover:bg-slate-700 rounded transition-colors"
        >
          <ChevronRight size={20} className="text-slate-400" />
        </button>
        {pageData.map((page) => (
          <button
            key={page.id}
            onClick={() => onSelectPage(page.id)}
            title={page.name}
            className={`w-8 h-8 rounded flex items-center justify-center transition-colors text-xs font-bold ${
              currentPageId === page.id
                ? 'bg-blue-500 text-white'
                : 'bg-slate-700 text-slate-400 hover:bg-slate-600'
            }`}
          >
            {page.name.charAt(0)}
          </button>
        ))}
      </div>
    );
  }

  return (
    <div className="w-60 bg-slate-900 border-r border-slate-700 flex flex-col text-slate-100 h-full">
      {/* 顶部工具栏 */}
      <div className="p-4 border-b border-slate-700">
        <div className="flex gap-2 mb-3">
          <div className="flex-1 relative">
            <Search size={16} className="absolute left-2 top-2.5 text-slate-500" />
            <input
              type="text"
              placeholder="搜索页面..."
              className="w-full bg-slate-800 border border-slate-700 rounded px-3 py-2 pl-8 text-sm placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <button
            onClick={onToggleCollapse}
            className="p-2 hover:bg-slate-800 rounded transition-colors"
          >
            <ChevronLeft size={16} />
          </button>
        </div>

        {/* 视图切换按钮 */}
        <div className="flex gap-2">
          <button
            onClick={() => onChangeViewMode('list')}
            className={`flex-1 px-3 py-2 rounded text-xs font-medium transition-colors ${
              viewMode === 'list'
                ? 'bg-blue-600 text-white'
                : 'bg-slate-800 text-slate-400 hover:bg-slate-700'
            }`}
          >
            列表
          </button>
          <button
            onClick={() => onChangeViewMode('flow')}
            className={`flex-1 px-3 py-2 rounded text-xs font-medium transition-colors ${
              viewMode === 'flow'
                ? 'bg-blue-600 text-white'
                : 'bg-slate-800 text-slate-400 hover:bg-slate-700'
            }`}
          >
            流程图
          </button>
        </div>
      </div>

      {/* 页面列表视图 */}
      {viewMode === 'list' && (
        <div className="flex-1 overflow-y-auto">
          {pageData.map((page) => {
            const isSelected = currentPageId === page.id;
            const statusColor = {
              designing: 'bg-gray-400',
              reviewing: 'bg-yellow-400',
              confirmed: 'bg-green-400',
            }[page.status];

            return (
              <div key={page.id}>
                <button
                  onClick={() => onSelectPage(page.id)}
                  className={`w-full px-4 py-3 text-left text-sm font-medium transition-colors flex items-center justify-between border-l-4 ${
                    isSelected
                      ? 'border-l-blue-500 bg-slate-800 text-white'
                      : 'border-l-transparent text-slate-400 hover:bg-slate-800'
                  }`}
                >
                  <span>{page.name}</span>
                  <div className="flex items-center gap-2">
                    <span className={`w-2 h-2 rounded-full ${statusColor}`} title={page.status} />
                    <span className="text-xs text-slate-500">
                      {page.type === 'modal' ? '⬜' : page.type === 'flow' ? '🔄' : '📄'}
                    </span>
                  </div>
                </button>
              </div>
            );
          })}
        </div>
      )}

      {/* 流程图视图 */}
      {viewMode === 'flow' && (
        <div className="flex-1 overflow-y-auto p-4">
          <svg className="w-full h-full min-h-96 border border-slate-700 rounded bg-slate-800" viewBox="0 0 200 400">
            {/* 登录节点 */}
            <g
              onClick={() => onSelectPage('login')}
              className={`cursor-pointer ${currentPageId === 'login' ? 'opacity-100' : 'opacity-60 hover:opacity-80'}`}
            >
              <rect x="50" y="20" width="100" height="40" fill="#2563EB" rx="4" />
              <text x="100" y="45" textAnchor="middle" fill="white" fontSize="12" fontWeight="bold">
                登录页
              </text>
            </g>

            {/* 箭头：登录 → 注册 */}
            <line x1="75" y1="60" x2="75" y2="100" stroke="#64748B" strokeWidth="1" markerEnd="url(#arrowhead)" />

            {/* 注册节点 */}
            <g
              onClick={() => onSelectPage('register')}
              className={`cursor-pointer ${currentPageId === 'register' ? 'opacity-100' : 'opacity-60 hover:opacity-80'}`}
            >
              <rect x="30" y="100" width="90" height="40" fill="#F97316" rx="4" />
              <text x="75" y="125" textAnchor="middle" fill="white" fontSize="12" fontWeight="bold">
                注册页
              </text>
            </g>

            {/* 箭头：登录 → 找回密码 */}
            <line x1="125" y1="60" x2="125" y2="100" stroke="#64748B" strokeWidth="1" markerEnd="url(#arrowhead)" />

            {/* 找回密码节点 */}
            <g
              onClick={() => onSelectPage('forgot-password')}
              className={`cursor-pointer ${currentPageId === 'forgot-password' ? 'opacity-100' : 'opacity-60 hover:opacity-80'}`}
            >
              <rect x="100" y="100" width="100" height="40" fill="#8B5CF6" rx="4" />
              <text x="150" y="125" textAnchor="middle" fill="white" fontSize="12" fontWeight="bold">
                找回密码
              </text>
            </g>

            {/* 箭头：注册 → 登录（返回） */}
            <path d="M 50 140 Q 50 180 100 180" fill="none" stroke="#64748B" strokeWidth="1" markerEnd="url(#arrowhead)" />
            <text x="30" y="160" fontSize="10" fill="#64748B">
              返回
            </text>

            {/* 箭头：找回密码 → 登录（返回） */}
            <path d="M 150 140 Q 150 180 100 180" fill="none" stroke="#64748B" strokeWidth="1" markerEnd="url(#arrowhead)" />
            <text x="160" y="160" fontSize="10" fill="#64748B">
              返回
            </text>

            {/* 登录成功节点 */}
            <g
              onClick={() => onSelectPage('home')}
              className={`cursor-pointer ${currentPageId === 'home' ? 'opacity-100' : 'opacity-60 hover:opacity-80'}`}
            >
              <rect x="50" y="280" width="100" height="40" fill="#10B981" rx="4" />
              <text x="100" y="305" textAnchor="middle" fill="white" fontSize="12" fontWeight="bold">
                首页（成功）
              </text>
            </g>

            {/* 箭头：登录 → 首页 */}
            <line x1="100" y1="180" x2="100" y2="280" stroke="#64748B" strokeWidth="1" markerEnd="url(#arrowhead)" />
            <text x="110" y="235" fontSize="10" fill="#64748B">
              登录
            </text>

            {/* SVG 箭头定义 */}
            <defs>
              <marker id="arrowhead" markerWidth="10" markerHeight="10" refX="5" refY="5" orient="auto">
                <polygon points="0 0, 10 5, 0 10" fill="#64748B" />
              </marker>
            </defs>
          </svg>
        </div>
      )}
    </div>
  );
};

// ============================================================================
// 中栏：原型预览
// ============================================================================

interface CenterPreviewProps {
  currentPage: IPageItem;
  onNavigate: (pageId: string) => void;
  onBack: () => void;
  zoom: number;
  onZoomChange: (zoom: number) => void;
  showDeviceFrame: boolean;
  onToggleDeviceFrame: () => void;
  navStack: string[];
}

const CenterPreview: React.FC<CenterPreviewProps> = ({
  currentPage,
  onNavigate,
  onBack,
  zoom,
  onZoomChange,
  showDeviceFrame,
  onToggleDeviceFrame,
  navStack,
}) => {
  const Prototype = currentPage.prototype;
  const iframeWidth = 375;
  const iframeHeight = 812;

  return (
    <div className="flex-1 bg-slate-100 flex flex-col">
      {/* 顶部工具栏 */}
      <div className="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-6 gap-4">
        {/* 缩放控制 */}
        <div className="flex items-center gap-2">
          <button
            onClick={() => onZoomChange(0.5)}
            className={`px-3 py-1 rounded text-sm font-medium transition-colors ${
              zoom === 0.5
                ? 'bg-blue-600 text-white'
                : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
            }`}
          >
            50%
          </button>
          <button
            onClick={() => onZoomChange(0.75)}
            className={`px-3 py-1 rounded text-sm font-medium transition-colors ${
              zoom === 0.75
                ? 'bg-blue-600 text-white'
                : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
            }`}
          >
            75%
          </button>
          <button
            onClick={() => onZoomChange(1)}
            className={`px-3 py-1 rounded text-sm font-medium transition-colors ${
              zoom === 1
                ? 'bg-blue-600 text-white'
                : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
            }`}
          >
            100%
          </button>
          <button
            onClick={() => onZoomChange(1.25)}
            className={`px-3 py-1 rounded text-sm font-medium transition-colors ${
              zoom === 1.25
                ? 'bg-blue-600 text-white'
                : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
            }`}
          >
            125%
          </button>
        </div>

        {/* 设备外壳开关 */}
        <button
          onClick={onToggleDeviceFrame}
          className={`px-4 py-2 rounded text-sm font-medium transition-colors flex items-center gap-2 ${
            showDeviceFrame
              ? 'bg-blue-600 text-white'
              : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
          }`}
        >
          📱 {showDeviceFrame ? 'iPhone' : '无框'}
        </button>

        {/* 面包屑 */}
        <div className="flex-1 flex items-center gap-2 text-sm text-slate-600">
          <Home size={16} />
          <span>/</span>
          <span className="font-medium text-slate-900">{currentPage.name}</span>
        </div>

        {/* 页面信息 */}
        <div className="text-xs text-slate-500">
          {navStack.length > 1 && <span className="text-blue-600">{navStack.length - 1} 步</span>}
        </div>
      </div>

      {/* 预览区域 */}
      <div className="flex-1 overflow-auto flex items-center justify-center p-6">
        <div
          style={{
            transform: `scale(${zoom})`,
            transformOrigin: 'top center',
            transition: 'transform 200ms ease-out',
          }}
          className="relative bg-white rounded-2xl shadow-2xl overflow-hidden"
        >
          {/* iPhone 外壳 */}
          {showDeviceFrame ? (
            <div className="relative" style={{ width: `${iframeWidth}px`, height: `${iframeHeight}px` }}>
              {/* 外壳背框 */}
              <div className="absolute inset-0 border-8 border-black rounded-3xl pointer-events-none bg-black" />
              {/* 内容 */}
              <div className="absolute inset-8 bg-white rounded-3xl overflow-hidden">
                <Prototype onNavigate={onNavigate} onBack={onBack} />
              </div>
            </div>
          ) : (
            <div style={{ width: `${iframeWidth}px`, height: `${iframeHeight}px` }}>
              <Prototype onNavigate={onNavigate} onBack={onBack} />
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

// ============================================================================
// 右栏：PRD + 评论
// ============================================================================

interface RightPanelProps {
  currentPage: IPageItem;
  isCollapsed: boolean;
  onToggleCollapse: () => void;
  width: number;
  onWidthChange: (width: number) => void;
  comments: Comment[];
  onAddComment: (text: string) => void;
}

const RightPanel: React.FC<RightPanelProps> = ({
  currentPage,
  isCollapsed,
  onToggleCollapse,
  width,
  onWidthChange,
  comments,
  onAddComment,
}) => {
  const [activeTab, setActiveTab] = React.useState<'prd' | 'comments'>('prd');
  const [commentText, setCommentText] = React.useState('');
  const [isDragging, setIsDragging] = React.useState(false);

  const handleMouseDown = () => {
    setIsDragging(true);
  };

  React.useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (!isDragging) return;
      const newWidth = window.innerWidth - e.clientX;
      if (newWidth >= 320 && newWidth <= 600) {
        onWidthChange(newWidth);
      }
    };

    const handleMouseUp = () => {
      setIsDragging(false);
    };

    window.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('mouseup', handleMouseUp);
    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('mouseup', handleMouseUp);
    };
  }, [isDragging, onWidthChange]);

  if (isCollapsed) {
    return (
      <div className="w-12 bg-slate-100 border-l border-slate-200 flex items-center justify-center">
        <button
          onClick={onToggleCollapse}
          className="p-2 hover:bg-slate-200 rounded transition-colors"
        >
          <ChevronLeft size={20} className="text-slate-600" />
        </button>
      </div>
    );
  }

  const pageComments = comments.filter((c) => c.pageId === currentPage.id);

  return (
    <div className="flex">
      {/* 拖拽句柄 */}
      <div
        onMouseDown={handleMouseDown}
        className={`w-1 bg-slate-300 hover:bg-blue-500 cursor-col-resize transition-colors ${
          isDragging ? 'bg-blue-500' : ''
        }`}
      />

      {/* 右栏内容 */}
      <div
        style={{ width: `${width}px` }}
        className="bg-white border-l border-slate-200 flex flex-col"
      >
        {/* Tab 栏 */}
        <div className="flex border-b border-slate-200 bg-slate-50">
          <button
            onClick={() => setActiveTab('prd')}
            className={`flex-1 px-4 py-3 text-sm font-medium transition-colors border-b-2 ${
              activeTab === 'prd'
                ? 'text-blue-600 border-b-blue-600'
                : 'text-slate-600 border-b-transparent hover:text-slate-900'
            }`}
          >
            PRD 文档
          </button>
          <button
            onClick={() => setActiveTab('comments')}
            className={`flex-1 px-4 py-3 text-sm font-medium transition-colors border-b-2 relative ${
              activeTab === 'comments'
                ? 'text-blue-600 border-b-blue-600'
                : 'text-slate-600 border-b-transparent hover:text-slate-900'
            }`}
          >
            评论
            {pageComments.length > 0 && (
              <span className="absolute top-2 right-2 bg-orange-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                {pageComments.length}
              </span>
            )}
          </button>
          <button
            onClick={onToggleCollapse}
            className="px-4 py-3 hover:bg-slate-100 rounded-tl transition-colors"
          >
            <ChevronLeft size={16} className="text-slate-600" />
          </button>
        </div>

        {/* PRD Tab */}
        {activeTab === 'prd' && (
          <div className="flex-1 overflow-y-auto p-4 prose prose-sm max-w-none">
            <div className="text-slate-700 text-sm leading-relaxed">
              {currentPage.prdContent.split('\n').map((line, i) => {
                if (line.startsWith('# ')) {
                  return (
                    <h1 key={i} className="text-xl font-bold mt-4 mb-2">
                      {line.replace('# ', '')}
                    </h1>
                  );
                }
                if (line.startsWith('## ')) {
                  return (
                    <h2 key={i} className="text-lg font-semibold mt-3 mb-2">
                      {line.replace('## ', '')}
                    </h2>
                  );
                }
                if (line.startsWith('### ')) {
                  return (
                    <h3 key={i} className="text-base font-semibold mt-2 mb-1">
                      {line.replace('### ', '')}
                    </h3>
                  );
                }
                if (line.startsWith('- ')) {
                  return (
                    <li key={i} className="ml-4">
                      {line.replace('- ', '')}
                    </li>
                  );
                }
                if (line.startsWith('| ')) {
                  return null; // 简化表格显示
                }
                if (line === '') {
                  return <br key={i} />;
                }
                if (line.includes('[AI 补全]')) {
                  return (
                    <p key={i} className="text-xs italic text-orange-600 bg-orange-50 px-2 py-1 rounded">
                      {line}
                    </p>
                  );
                }
                return (
                  <p key={i} className="mb-2">
                    {line}
                  </p>
                );
              })}
            </div>
          </div>
        )}

        {/* 评论 Tab */}
        {activeTab === 'comments' && (
          <div className="flex-1 flex flex-col overflow-hidden">
            {/* 评论列表 */}
            <div className="flex-1 overflow-y-auto p-4 space-y-3">
              {pageComments.length === 0 ? (
                <p className="text-center text-slate-500 text-sm py-8">
                  暂无评论，添加一条吧
                </p>
              ) : (
                pageComments.map((comment, idx) => (
                  <div key={idx} className="bg-slate-50 rounded p-3 border border-slate-200">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm font-medium text-slate-900">{comment.author}</span>
                      <span className="text-xs text-slate-500">{comment.time}</span>
                    </div>
                    <p className="text-sm text-slate-700">{comment.text}</p>
                  </div>
                ))
              )}
            </div>

            {/* 评论输入 */}
            <div className="border-t border-slate-200 p-3 space-y-2">
              <textarea
                placeholder="添加评论..."
                value={commentText}
                onChange={(e) => setCommentText(e.target.value)}
                className="w-full bg-slate-50 border border-slate-200 rounded p-2 text-sm placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none"
                rows={3}
              />
              <button
                onClick={() => {
                  if (commentText.trim()) {
                    onAddComment(commentText);
                    setCommentText('');
                  }
                }}
                disabled={!commentText.trim()}
                className="w-full bg-blue-600 text-white py-2 rounded text-sm font-medium hover:bg-blue-700 disabled:bg-slate-300 transition-colors"
              >
                发送
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

// ============================================================================
// 主组件：完整原型审查系统
// ============================================================================

export default function PrototypeReviewPage() {
  // 导航栈
  const [navStack, setNavStack] = React.useState<string[]>(['login']);
  const currentPageId = navStack[navStack.length - 1];
  const currentPage = pageData.find((p) => p.id === currentPageId) || pageData[0];

  // 左栏
  const [leftCollapsed, setLeftCollapsed] = React.useState(false);
  const [viewMode, setViewMode] = React.useState<'list' | 'flow'>('list');

  // 右栏
  const [rightCollapsed, setRightCollapsed] = React.useState(false);
  const [rightWidth, setRightWidth] = React.useState(420);

  // 中栏
  const [zoom, setZoom] = React.useState(1);
  const [showDeviceFrame, setShowDeviceFrame] = React.useState(true);

  // Toast 和评论
  const [toasts, setToasts] = React.useState<Toast[]>([]);
  const [comments, setComments] = React.useState<Comment[]>([]);

  // 导航处理
  const handleNavigate = (pageId: string) => {
    const pageExists = pageData.find((p) => p.id === pageId);
    if (!pageExists) {
      const newToast: Toast = {
        id: Math.random().toString(),
        message: `页面 [${pageId}] 尚未定义`,
        type: 'error',
      };
      setToasts((prev) => [...prev, newToast]);
      return;
    }
    setNavStack((prev) => [...prev, pageId]);
    // 同步到 URL
    window.history.pushState({ pageId }, '', `?page=${pageId}`);
  };

  const handleBack = () => {
    if (navStack.length > 1) {
      setNavStack((prev) => prev.slice(0, -1));
      const prevPageId = navStack[navStack.length - 2];
      window.history.replaceState({ pageId: prevPageId }, '', `?page=${prevPageId}`);
    }
  };

  const handleSelectPage = (pageId: string) => {
    setNavStack([pageId]);
    window.history.pushState({ pageId }, '', `?page=${pageId}`);
  };

  const handleAddComment = (text: string) => {
    const newComment: Comment = {
      pageId: currentPageId,
      author: 'PM',
      text,
      time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' }),
    };
    setComments((prev) => [...prev, newComment]);
  };

  // URL 同步
  React.useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const pageParam = params.get('page');
    if (pageParam && pageData.find((p) => p.id === pageParam)) {
      setNavStack([pageParam]);
    }
  }, []);

  return (
    <div className="flex h-screen bg-slate-50 overflow-hidden">
      {/* 全局样式 */}
      <style>{`
        @keyframes slide-up {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .animate-slide-up {
          animation: slide-up 0.3s ease-out;
        }
      `}</style>

      {/* 左栏：导航 */}
      <LeftSidebar
        pageData={pageData}
        currentPageId={currentPageId}
        onSelectPage={handleSelectPage}
        isCollapsed={leftCollapsed}
        onToggleCollapse={() => setLeftCollapsed(!leftCollapsed)}
        viewMode={viewMode}
        onChangeViewMode={setViewMode}
      />

      {/* 中栏：预览 */}
      <CenterPreview
        currentPage={currentPage}
        onNavigate={handleNavigate}
        onBack={handleBack}
        zoom={zoom}
        onZoomChange={setZoom}
        showDeviceFrame={showDeviceFrame}
        onToggleDeviceFrame={() => setShowDeviceFrame(!showDeviceFrame)}
        navStack={navStack}
      />

      {/* 右栏：文档 + 评论 */}
      <RightPanel
        currentPage={currentPage}
        isCollapsed={rightCollapsed}
        onToggleCollapse={() => setRightCollapsed(!rightCollapsed)}
        width={rightWidth}
        onWidthChange={setRightWidth}
        comments={comments}
        onAddComment={handleAddComment}
      />

      {/* Toast 系统 */}
      <Toast toasts={toasts} onRemove={(id) => setToasts((prev) => prev.filter((t) => t.id !== id))} />
    </div>
  );
}
