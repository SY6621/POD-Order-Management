/**
 * 后端 API 服务
 * 调用 FastAPI 后端接口
 */

const API_BASE_URL = 'http://localhost:8000'

/**
 * 生成效果图
 * @param {Object} params - 参数
 * @param {string} params.order_id - 订单ID
 * @param {string} params.shape - 形状 (bone/heart/circle)
 * @param {string} params.color - 颜色 (G/S/B)
 * @param {string} params.size - 尺寸 (large/small)
 * @param {string} params.text_front - 正面文字
 * @param {string} params.text_back - 背面文字
 * @param {string} params.font_code - 字体代码
 * @returns {Promise<Object>} - 生成结果
 */
export async function generateEffectImage(params) {
  const response = await fetch(`${API_BASE_URL}/api/effect-image/generate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(params),
  })
  
  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || '生成效果图失败')
  }
  
  return response.json()
}

/**
 * 查看效果图
 * @param {string} filename - 文件名
 * @returns {string} - 图片URL
 */
export function getEffectImageUrl(filename) {
  return `${API_BASE_URL}/api/effect-image/view/${filename}`
}

/**
 * 更新订单状态
 * @param {string} orderId - 订单ID
 * @param {string} status - 新状态
 * @returns {Promise<Object>} - 更新结果
 */
export async function updateOrderStatus(orderId, status) {
  const response = await fetch(`${API_BASE_URL}/api/order/update-status`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ order_id: orderId, status }),
  })
  
  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || '更新状态失败')
  }
  
  return response.json()
}

/**
 * 发送确认邮件
 * @param {Object} params - 参数
 * @param {string} params.order_id - 订单ID
 * @param {string} params.to_email - 客户邮箱
 * @param {string} params.customer_name - 客户名称
 * @param {string} params.product_info - 产品信息
 * @param {string} params.effect_image_path - 效果图路径
 * @returns {Promise<Object>} - 发送结果
 */
export async function sendConfirmationEmail(params) {
  const response = await fetch(`${API_BASE_URL}/api/email/send-confirmation`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(params),
  })
  
  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || '发送邮件失败')
  }
  
  return response.json()
}

/**
 * 健康检查
 * @returns {Promise<Object>} - 状态
 */
export async function healthCheck() {
  const response = await fetch(`${API_BASE_URL}/health`)
  return response.json()
}

export default {
  generateEffectImage,
  getEffectImageUrl,
  updateOrderStatus,
  sendConfirmationEmail,
  healthCheck,
}
