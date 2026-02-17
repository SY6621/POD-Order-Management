<template>
  <div class="app-container">
    <!-- 头部 -->
    <header class="header">
      <div class="header-inner">
        <div class="header-left">
          <div class="logo-cube">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
              <polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline>
              <line x1="12" y1="22.08" x2="12" y2="12"></line>
            </svg>
          </div>
          <div>
            <div class="header-title-main">生产订单管理系统</div>
            <div class="header-title-sub">生产订单与邮件管理平台</div>
          </div>
        </div>
      </div>
    </header>

    <!-- 主体内容 -->
    <div class="main-wrapper">
      <!-- 左侧导航 -->
      <aside class="left-sider">
        <div class="nav-card">
          <div class="tab-vertical">
            <button class="tab" :class="{ 'is-active': activeTab === 'dashboard' }" @click="switchTab('dashboard')">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="7" height="9" x="3" y="3" rx="1"></rect><rect width="7" height="5" x="14" y="3" rx="1"></rect><rect width="7" height="9" x="14" y="12" rx="1"></rect><rect width="7" height="5" x="3" y="16" rx="1"></rect></svg>
              仪表盘总览
            </button>
            <button class="tab" :class="{ 'is-active': activeTab === 'pending' }" @click="switchTab('pending')">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 6v6l4 2"></path><circle cx="12" cy="12" r="10"></circle></svg>
              待确认订单
            </button>
            <button class="tab" :class="{ 'is-active': activeTab === 'producing' }" @click="switchTab('producing')">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m15 12-9.373 9.373a1 1 0 0 1-3.001-3L12 9"></path><path d="m18 15 4-4"></path><path d="m21.5 11.5-1.914-1.914A2 2 0 0 1 19 8.172v-.344a2 2 0 0 0-.586-1.414l-1.657-1.657A6 6 0 0 0 12.516 3H9l1.243 1.243A6 6 0 0 1 12 8.485V10l2 2h1.172a2 2 0 0 1 1.414.586L18.5 14.5"></path></svg>
              生产中订单
            </button>
            <button class="tab" :class="{ 'is-active': activeTab === 'completed' }" @click="switchTab('completed')">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21.801 10A10 10 0 1 1 17 3.335"></path><path d="m9 11 3 3L22 4"></path></svg>
              已完成订单
            </button>
            <button class="tab" :class="{ 'is-active': activeTab === 'templates' }" @click="switchTab('templates')">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m22 7-8.991 5.727a2 2 0 0 1-2.009 0L2 7"></path><rect x="2" y="4" width="20" height="16" rx="2"></rect></svg>
              邮件模板
            </button>
          </div>
        </div>

        <div class="mini-stats">
          <div class="stat-item">
            <div class="stat-ring stat-ring-total"></div>
            <div class="stat-info">
              <span class="stat-val">{{ stats.total }}</span>
              <span class="stat-lab">总订单</span>
            </div>
          </div>
          <div class="stat-item">
            <div class="stat-ring stat-ring-pending"></div>
            <div class="stat-info">
              <span class="stat-val">{{ stats.pending }}</span>
              <span class="stat-lab">待处理</span>
            </div>
          </div>
          <div class="stat-item">
            <div class="stat-ring stat-ring-producing"></div>
            <div class="stat-info">
              <span class="stat-val">{{ stats.producing }}</span>
              <span class="stat-lab">生产中</span>
            </div>
          </div>
          <div class="stat-item">
            <div class="stat-ring stat-ring-done"></div>
            <div class="stat-info">
              <span class="stat-val">{{ stats.completed }}</span>
              <span class="stat-lab">已交付</span>
            </div>
          </div>
        </div>
      </aside>

      <!-- 右侧内容区 -->
      <main class="right-content">
        <!-- 仪表盘 -->
        <section class="panel" :class="{ 'is-active': activeTab === 'dashboard' }">
          <p class="dashboard-intro">仪表盘总览：待确认订单、生产中订单、已完成订单</p>
          
          <div class="dashboard-sections">
            <!-- 版块一：待确认订单 -->
            <div>
              <div class="section-header">
                <div>
                  <h2 class="section-title">最近订单 \ 待确认订单</h2>
                  <p class="section-sub">最新的生产订单</p>
                </div>
                <button class="section-link" @click="switchTab('pending')">查看全部 →</button>
              </div>
              <div class="search-row">
                <div class="search-wrap">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21 21-4.34-4.34"></path><circle cx="11" cy="11" r="8"></circle></svg>
                  <input type="search" class="search-input" placeholder="搜索订单号、客户名称或产品..." v-model="searchPending">
                </div>
              </div>
              <div class="table-wrap">
                <div class="table-scroll">
                  <table>
                    <thead>
                      <tr>
                        <th>订单ID</th>
                        <th>客户名称</th>
                        <th>产品</th>
                        <th>设计稿件</th>
                        <th>确认邮件</th>
                        <th>数量</th>
                        <th>状态</th>
                        <th>创建日期</th>
                        <th>操作</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="order in pendingOrdersPreview" :key="order.id">
                        <td>#{{ order.etsy_order_id }}</td>
                        <td class="cell-muted">{{ order.customer_name }}</td>
                        <td class="cell-muted">{{ order.sku_mapping?.sku_code || '-' }}</td>
                        <td><button class="btn-icon" @click="handleGenerateEffectImage(order)" :disabled="generating"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"></rect><circle cx="9" cy="9" r="2"></circle><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"></path></svg> {{ generating ? '生成中...' : '生成效果图' }}</button></td>
                        <td><button class="btn-icon" @click="handleGenerateEmail(order)"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m22 7-8.991 5.727a2 2 0 0 1-2.009 0L2 7"></path><rect x="2" y="4" width="20" height="16" rx="2"></rect></svg> 生成邮件</button></td>
                        <td>{{ order.quantity }}</td>
                        <td><span class="badge" :class="getStatusBadgeClass(order.status)">{{ getStatusText(order.status) }}</span></td>
                        <td>{{ formatDate(order.created_at) }}</td>
                        <td><button class="btn-ghost" @click="handleCreateOrder(order)">创建订单</button></td>
                      </tr>
                      <tr v-if="pendingOrdersPreview.length === 0">
                        <td colspan="9" style="text-align: center; color: #999;">暂无数据</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>

            <!-- 版块二：生产中订单 -->
            <div>
              <div class="section-header">
                <div>
                  <h2 class="section-title">生产中订单</h2>
                  <p class="section-sub">订单由「待确认订单」创建完成后流转到此</p>
                </div>
                <button class="section-link" @click="switchTab('producing')">查看全部 →</button>
              </div>
              <div class="search-row">
                <div class="search-wrap">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21 21-4.34-4.34"></path><circle cx="11" cy="11" r="8"></circle></svg>
                  <input type="search" class="search-input" placeholder="搜索订单号、客户名称或产品..." v-model="searchProducing">
                </div>
              </div>
              <div class="table-wrap">
                <div class="table-scroll">
                  <table>
                    <thead>
                      <tr>
                        <th>客户名称</th>
                        <th>产品</th>
                        <th>生产表单</th>
                        <th>进度</th>
                        <th>数量</th>
                        <th>状态</th>
                        <th>物流面单</th>
                        <th>下单取货</th>
                        <th>创建日期</th>
                        <th>操作</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="order in producingOrdersPreview" :key="order.id">
                        <td class="cell-muted">{{ order.customer_name }}</td>
                        <td class="cell-muted">{{ order.sku_mapping?.sku_code || '-' }}</td>
                        <td><button class="btn-icon"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 22a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h8a2.4 2.4 0 0 1 1.704.706l3.588 3.588A2.4 2.4 0 0 1 20 8v12a2 2 0 0 1-2 2z"></path><path d="M14 2v5a1 1 0 0 0 1 1h5"></path><path d="M10 9H8"></path><path d="M16 13H8"></path><path d="M16 17H8"></path></svg> 生成表单</button></td>
                        <td><div class="progress-wrap"><div class="progress-bar"><div class="progress-fill" :style="{ width: order.progress + '%' }"></div></div><div class="progress-label">{{ order.progress }}%</div></div></td>
                        <td>{{ order.quantity }}</td>
                        <td><span class="badge" :class="getStatusBadgeClass(order.status)">{{ getStatusText(order.status) }}</span></td>
                        <td>
                          <button class="btn-icon"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2.062 12.348a1 1 0 0 1 0-.696 10.75 10.75 0 0 1 19.876 0 1 1 0 0 1 0 .696 10.75 10.75 0 0 1-19.876 0"></path><circle cx="12" cy="12" r="3"></circle></svg> 查看</button>
                          <button class="btn-icon"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 15V3"></path><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><path d="m7 10 5 5 5-5"></path></svg></button>
                        </td>
                        <td><button class="btn-ghost">当日下单</button></td>
                        <td>{{ formatDate(order.created_at) }}</td>
                        <td><button class="btn-ghost">物流取货</button></td>
                      </tr>
                      <tr v-if="producingOrdersPreview.length === 0">
                        <td colspan="10" style="text-align: center; color: #999;">暂无数据</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>

            <!-- 版块三：已完成订单 -->
            <div>
              <div class="section-header">
                <div>
                  <h2 class="section-title">已完成订单</h2>
                  <p class="section-sub">发货日起 30 天内订单；集成客户订单信息、效果图、往来邮件、生产表单</p>
                </div>
                <button class="section-link" @click="switchTab('completed')">查看全部 →</button>
              </div>
              <div class="search-row">
                <div class="search-wrap">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21 21-4.34-4.34"></path><circle cx="11" cy="11" r="8"></circle></svg>
                  <input type="search" class="search-input" placeholder="搜索订单号、客户名称或产品..." v-model="searchCompleted">
                </div>
              </div>
              <div class="table-wrap">
                <div class="table-scroll">
                  <table>
                    <thead>
                      <tr>
                        <th>订单ID</th>
                        <th>客户名称</th>
                        <th>产品</th>
                        <th>国家地址</th>
                        <th>发货日期</th>
                        <th>收货日期</th>
                        <th>物流送达</th>
                        <th>追评邮件</th>
                        <th>处理详情</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="order in completedOrdersPreview" :key="order.id">
                        <td>#{{ order.etsy_order_id }}</td>
                        <td class="cell-muted">{{ order.customer_name }}</td>
                        <td class="cell-muted">{{ order.sku_mapping?.sku_code || '-' }}</td>
                        <td class="cell-muted">{{ order.logistics?.country || '-' }}, {{ order.logistics?.city || '' }}</td>
                        <td>{{ formatDate(order.logistics?.shipped_at) }}</td>
                        <td>{{ formatDate(order.logistics?.delivered_at) }}</td>
                        <td>{{ getDeliveryStatusText(order.logistics?.delivery_status) }}</td>
                        <td><button class="btn-icon"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m22 7-8.991 5.727a2 2 0 0 1-2.009 0L2 7"></path><rect x="2" y="4" width="20" height="16" rx="2"></rect></svg> 查看</button></td>
                        <td><button class="btn-icon"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 22a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h8a2.4 2.4 0 0 1 1.704.706l3.588 3.588A2.4 2.4 0 0 1 20 8v12a2 2 0 0 1-2 2z"></path><path d="M14 2v5a1 1 0 0 0 1 1h5"></path><path d="M10 9H8"></path><path d="M16 13H8"></path><path d="M16 17H8"></path></svg> 处理详情</button></td>
                      </tr>
                      <tr v-if="completedOrdersPreview.length === 0">
                        <td colspan="9" style="text-align: center; color: #999;">暂无数据</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- 待确认订单页面 -->
        <section class="panel" :class="{ 'is-active': activeTab === 'pending' }">
          <h2 class="section-title">最近订单 \ 待确认订单</h2>
          <p class="section-sub">最新的生产订单</p>
          <div class="search-row" style="margin-top: 16px;">
            <div class="search-wrap">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21 21-4.34-4.34"></path><circle cx="11" cy="11" r="8"></circle></svg>
              <input type="search" class="search-input" placeholder="搜索订单号、客户名称或产品...">
            </div>
          </div>
          <div class="table-wrap">
            <div class="table-scroll">
              <table>
                <thead>
                  <tr>
                    <th>订单ID</th>
                    <th>客户名称</th>
                    <th>产品</th>
                    <th>设计稿件</th>
                    <th>确认邮件</th>
                    <th>进度</th>
                    <th>数量</th>
                    <th>状态</th>
                    <th>创建日期</th>
                    <th>交付日期</th>
                    <th>操作</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="order in pendingOrders" :key="order.id">
                    <td>#{{ order.etsy_order_id }}</td>
                    <td class="cell-muted">{{ order.customer_name }}</td>
                    <td class="cell-muted">{{ order.sku_mapping?.sku_code || '-' }}</td>
                    <td><button class="btn-icon"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"></rect><circle cx="9" cy="9" r="2"></circle><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"></path></svg> 生成效果图</button></td>
                    <td><button class="btn-icon"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m22 7-8.991 5.727a2 2 0 0 1-2.009 0L2 7"></path><rect x="2" y="4" width="20" height="16" rx="2"></rect></svg> 生成邮件</button></td>
                    <td><div class="progress-wrap"><div class="progress-bar"><div class="progress-fill" :style="{ width: order.progress + '%' }"></div></div><div class="progress-label">{{ order.progress }}%</div></div></td>
                    <td>{{ order.quantity }}</td>
                    <td><span class="badge" :class="getStatusBadgeClass(order.status)">{{ getStatusText(order.status) }}</span></td>
                    <td>{{ formatDate(order.created_at) }}</td>
                    <td>{{ formatDate(order.estimated_delivery) }}</td>
                    <td><button class="btn-ghost">创建订单</button> <button class="btn-ghost danger">取消订单</button></td>
                  </tr>
                  <tr v-if="pendingOrders.length === 0">
                    <td colspan="11" style="text-align: center; color: #999;">暂无数据</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </section>

        <!-- 生产中订单页面 -->
        <section class="panel" :class="{ 'is-active': activeTab === 'producing' }">
          <h2 class="section-title">生产中订单</h2>
          <p class="section-sub">由「待确认订单」创建完成后流转到此</p>
          <div class="search-row" style="margin-top: 16px;">
            <div class="search-wrap">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21 21-4.34-4.34"></path><circle cx="11" cy="11" r="8"></circle></svg>
              <input type="search" class="search-input" placeholder="搜索订单号、客户名称或产品...">
            </div>
          </div>
          <div class="table-wrap">
            <div class="table-scroll">
              <table>
                <thead>
                  <tr>
                    <th>客户名称</th>
                    <th>产品</th>
                    <th>生产表单</th>
                    <th>进度</th>
                    <th>数量</th>
                    <th>状态</th>
                    <th>物流面单</th>
                    <th>下单取货</th>
                    <th>创建日期</th>
                    <th>交付日期</th>
                    <th>操作</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="order in producingOrders" :key="order.id">
                    <td class="cell-muted">{{ order.customer_name }}</td>
                    <td class="cell-muted">{{ order.sku_mapping?.sku_code || '-' }}</td>
                    <td><button class="btn-icon"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 22a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h8a2.4 2.4 0 0 1 1.704.706l3.588 3.588A2.4 2.4 0 0 1 20 8v12a2 2 0 0 1-2 2z"></path><path d="M14 2v5a1 1 0 0 0 1 1h5"></path><path d="M10 9H8"></path><path d="M16 13H8"></path><path d="M16 17H8"></path></svg> 生成表单</button></td>
                    <td><div class="progress-wrap"><div class="progress-bar"><div class="progress-fill" :style="{ width: order.progress + '%' }"></div></div><div class="progress-label">{{ order.progress }}%</div></div></td>
                    <td>{{ order.quantity }}</td>
                    <td><span class="badge" :class="getStatusBadgeClass(order.status)">{{ getStatusText(order.status) }}</span></td>
                    <td>
                      <button class="btn-icon"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2.062 12.348a1 1 0 0 1 0-.696 10.75 10.75 0 0 1 19.876 0 1 1 0 0 1 0 .696 10.75 10.75 0 0 1-19.876 0"></path><circle cx="12" cy="12" r="3"></circle></svg> 查看</button>
                      <button class="btn-icon"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 15V3"></path><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><path d="m7 10 5 5 5-5"></path></svg></button>
                    </td>
                    <td><button class="btn-ghost">当日下单</button></td>
                    <td>{{ formatDate(order.created_at) }}</td>
                    <td>{{ formatDate(order.estimated_delivery) }}</td>
                    <td><button class="btn-ghost">物流取货</button></td>
                  </tr>
                  <tr v-if="producingOrders.length === 0">
                    <td colspan="11" style="text-align: center; color: #999;">暂无数据</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </section>

        <!-- 已完成订单页面 -->
        <section class="panel" :class="{ 'is-active': activeTab === 'completed' }">
          <h2 class="section-title">已完成订单</h2>
          <p class="section-sub">发货日起 30 天内订单</p>
          <div class="search-row" style="margin-top: 16px;">
            <div class="search-wrap">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21 21-4.34-4.34"></path><circle cx="11" cy="11" r="8"></circle></svg>
              <input type="search" class="search-input" placeholder="搜索订单号、客户名称或产品...">
            </div>
          </div>
          <div class="table-wrap">
            <div class="table-scroll">
              <table>
                <thead>
                  <tr>
                    <th>订单ID</th>
                    <th>客户名称</th>
                    <th>产品</th>
                    <th>国家地址</th>
                    <th>发货日期</th>
                    <th>收货日期</th>
                    <th>物流送达</th>
                    <th>追评邮件</th>
                    <th>处理详情</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="order in completedOrders" :key="order.id">
                    <td>#{{ order.etsy_order_id }}</td>
                    <td class="cell-muted">{{ order.customer_name }}</td>
                    <td class="cell-muted">{{ order.sku_mapping?.sku_code || '-' }}</td>
                    <td class="cell-muted">{{ order.logistics?.country || '-' }}, {{ order.logistics?.city || '' }}</td>
                    <td>{{ formatDate(order.logistics?.shipped_at) }}</td>
                    <td>{{ formatDate(order.logistics?.delivered_at) }}</td>
                    <td>{{ getDeliveryStatusText(order.logistics?.delivery_status) }}</td>
                    <td><button class="btn-icon"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m22 7-8.991 5.727a2 2 0 0 1-2.009 0L2 7"></path><rect x="2" y="4" width="20" height="16" rx="2"></rect></svg> 查看</button></td>
                    <td><button class="btn-icon"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 22a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h8a2.4 2.4 0 0 1 1.704.706l3.588 3.588A2.4 2.4 0 0 1 20 8v12a2 2 0 0 1-2 2z"></path><path d="M14 2v5a1 1 0 0 0 1 1h5"></path><path d="M10 9H8"></path><path d="M16 13H8"></path><path d="M16 17H8"></path></svg> 处理详情</button></td>
                  </tr>
                  <tr v-if="completedOrders.length === 0">
                    <td colspan="9" style="text-align: center; color: #999;">暂无数据</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </section>

        <!-- 邮件模板页面 -->
        <section class="panel" :class="{ 'is-active': activeTab === 'templates' }">
          <h2 class="section-title">邮件模板</h2>
          <p class="section-sub">确认邮件、物流耽误/丢件、追评模板</p>
          <div class="template-grid" style="margin-top: 16px;">
            <div class="template-card">
              <h4>确认邮件模板</h4>
              <p>客户确认订单或设计稿修改完成后的确认邮件</p>
              <button class="btn-icon"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 21h8"></path><path d="M21.174 6.812a1 1 0 0 0-3.986-3.987L3.842 16.174a2 2 0 0 0-.5.83l-1.321 4.352a.5.5 0 0 0 .623.622l4.353-1.32a2 2 0 0 0 .83-.497z"></path></svg> 编辑</button>
            </div>
            <div class="template-card">
              <h4>物流耽误 \ 丢件邮件模板</h4>
              <p>物流延迟或丢件时发送给客户的说明与补救邮件</p>
              <button class="btn-icon"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 21h8"></path><path d="M21.174 6.812a1 1 0 0 0-3.986-3.987L3.842 16.174a2 2 0 0 0-.5.83l-1.321 4.352a.5.5 0 0 0 .623.622l4.353-1.32a2 2 0 0 0 .83-.497z"></path></svg> 编辑</button>
            </div>
            <div class="template-card">
              <h4>追评邮件模板</h4>
              <p>收货后邀请客户评价的邮件模板</p>
              <button class="btn-icon"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 21h8"></path><path d="M21.174 6.812a1 1 0 0 0-3.986-3.987L3.842 16.174a2 2 0 0 0-.5.83l-1.321 4.352a.5.5 0 0 0 .623.622l4.353-1.32a2 2 0 0 0 .83-.497z"></path></svg> 编辑</button>
            </div>
          </div>
        </section>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useOrderStore } from '../../stores/orderStore'
import { generateEffectImage, getEffectImageUrl, sendConfirmationEmail } from '../../utils/api'

const orderStore = useOrderStore()

// 当前激活的选项卡
const activeTab = ref('dashboard')

// 加载状态
const generating = ref(false)

// 搜索关键词
const searchPending = ref('')
const searchProducing = ref('')
const searchCompleted = ref('')

// 统计数据
const stats = ref({
  total: 0,
  pending: 0,
  producing: 0,
  completed: 0
})

// 订单数据
const pendingOrders = ref([])
const producingOrders = ref([])
const completedOrders = ref([])

// 仪表盘预览数据（只显示前2条）
const pendingOrdersPreview = computed(() => pendingOrders.value.slice(0, 2))
const producingOrdersPreview = computed(() => producingOrders.value.slice(0, 2))
const completedOrdersPreview = computed(() => completedOrders.value.slice(0, 2))

// 切换选项卡
const switchTab = (tab) => {
  activeTab.value = tab
}

// 状态文本映射（与数据库约束一致）
const getStatusText = (status) => {
  const map = {
    pending: '待确认',
    effect_sent: '效果图已发',
    producing: '生产中',
    delivered: '已送达'
  }
  return map[status] || status
}

// 状态样式映射
const getStatusBadgeClass = (status) => {
  const map = {
    pending: 'badge-pending',
    effect_sent: 'badge-pending',
    producing: 'badge-producing',
    delivered: 'badge-done'
  }
  return map[status] || 'badge-new'
}

// 物流状态文本
const getDeliveryStatusText = (status) => {
  const map = {
    pending: '待发货',
    shipped: '已发货',
    in_transit: '运输中',
    delivered: '已送达',
    failed: '配送失败'
  }
  return map[status] || '-'
}

// 格式化日期
const formatDate = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleDateString('zh-CN')
}

// 加载数据
const loadData = async () => {
  try {
    console.log('开始加载订单数据...')
    
    // 获取统计数据
    const statsData = await orderStore.getOrderStats()
    stats.value = {
      total: statsData.total || 0,
      pending: statsData.pending || 0,
      producing: statsData.producing || 0,
      completed: statsData.completed || 0
    }
    console.log('统计数据:', stats.value)

    // 获取待确认订单
    pendingOrders.value = await orderStore.getPendingOrders() || []
    console.log('待确认订单:', pendingOrders.value.length)

    // 获取生产中订单
    producingOrders.value = await orderStore.getProducingOrders() || []
    console.log('生产中订单:', producingOrders.value.length)

    // 获取已完成订单
    completedOrders.value = await orderStore.getCompletedOrders() || []
    console.log('已完成订单:', completedOrders.value.length)
  } catch (error) {
    console.error('加载数据失败:', error)
  }
}

// 页面加载时获取数据
onMounted(() => {
  loadData()
})

// ============ 功能按钮处理 ============

// 生成效果图
const handleGenerateEffectImage = async (order) => {
  if (generating.value) return
  
  generating.value = true
  try {
    console.log('开始生成效果图:', order.etsy_order_id)
    
    const result = await generateEffectImage({
      order_id: order.etsy_order_id,
      shape: 'bone',  // TODO: 从 SKU 解析
      color: 'G',     // TODO: 从 SKU 解析
      size: 'large',  // TODO: 从 SKU 解析
      text_front: order.front_text || 'Sample Text',
      text_back: order.back_text || '',
      font_code: 'F-01'
    })
    
    console.log('✅ 效果图生成成功:', result)
    alert(`效果图生成成功！\n文件: ${result.front_svg}`)
    
  } catch (error) {
    console.error('❌ 效果图生成失败:', error)
    alert('效果图生成失败: ' + error.message)
  } finally {
    generating.value = false
  }
}

// 生成邮件
const sendingEmail = ref(false)

const handleGenerateEmail = async (order) => {
  if (sendingEmail.value) return
  sendingEmail.value = true
  
  try {
    // 构建产品信息
    const productInfo = [
      order.shape || 'bone',
      order.color || 'gold',
      order.size || 'large',
      order.front_text || ''
    ].filter(Boolean).join(' - ')
    
    const result = await sendConfirmationEmail({
      order_id: order.etsy_order_id,
      to_email: order.customer_email || 'test@example.com',
      customer_name: order.customer_name || 'Customer',
      product_info: productInfo,
      effect_image_path: order.effect_image_path || ''
    })
    
    alert(`邮件发送成功！\n${result.message}`)
  } catch (error) {
    console.error('发送邮件失败:', error)
    alert('发送邮件失败: ' + error.message)
  } finally {
    sendingEmail.value = false
  }
}

// 生成生产表单
const handleGenerateForm = async (order) => {
  alert('功能开发中: 生成表单')
}

// 创建订单
const handleCreateOrder = async (order) => {
  alert('功能开发中: 创建订单')
}

// 物流取货
const handleLogisticsPickup = async (order) => {
  alert('功能开发中: 物流取货')
}
</script>

<style scoped>
:root {
  --page-width: 1400px;
  --bg: #f8f9fa;
  --panel-bg: #ffffff;
  --text: #000000;
  --text-muted: #666666;
  --text-soft: #999999;
  --border: #e5e5e5;
  --border-soft: #dddddd;
  --card-shadow: 0 1px 3px rgba(0,0,0,0.06);
  --radius: 8px;
  --radius-sm: 6px;
  --radius-pill: 999px;
  --status-new: #f5f5f5;
  --status-new-border: #e0e0e0;
  --status-pending: #ebebeb;
  --status-pending-border: #d0d0d0;
  --status-producing: #d8d8d8;
  --status-producing-border: #b8b8b8;
  --status-done: #333333;
  --status-done-fg: #ffffff;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

.app-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  background: #f8f9fa;
  color: #000000;
  font-size: 14px;
  line-height: 1.45;
  overflow: hidden;
  -webkit-font-smoothing: antialiased;
}

.header {
  height: 64px;
  background: #ffffff;
  border-bottom: 1px solid #e5e5e5;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 24px;
  flex-shrink: 0;
}

.header-inner {
  width: 100%;
  max-width: 1400px;
  display: flex;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 14px;
}

.logo-cube {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  border: 1px solid #e5e5e5;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  background: linear-gradient(145deg, #fafafa, #f0f0f0);
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo-cube svg {
  width: 22px;
  height: 22px;
  color: #666666;
  stroke-width: 1.5;
}

.header-title-main {
  font-size: 18px;
  font-weight: 600;
  letter-spacing: 0.02em;
}

.header-title-sub {
  font-size: 11px;
  color: #999999;
  letter-spacing: 0.06em;
  margin-top: 2px;
}

.main-wrapper {
  display: flex;
  flex: 1;
  padding: 24px;
  gap: 24px;
  overflow: hidden;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
}

.left-sider {
  width: 240px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  gap: 20px;
  overflow-y: auto;
}

.right-content {
  flex: 1;
  background: #ffffff;
  border-radius: 8px;
  border: 1px solid #e5e5e5;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}

.nav-card {
  background: #ffffff;
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  padding: 12px;
}

.tab-vertical {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.tab {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  text-decoration: none;
  color: #666666;
  border-radius: 6px;
  transition: all 0.2s;
  border: none;
  background: none;
  width: 100%;
  cursor: pointer;
  font-size: 13px;
  text-align: left;
}

.tab svg {
  width: 18px;
  height: 18px;
  stroke-width: 1.5;
  flex-shrink: 0;
}

.tab:hover {
  background: #f5f5f5;
  color: #000000;
}

.tab.is-active {
  background: #f0f0f0;
  color: #000000;
  font-weight: 500;
}

.mini-stats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.stat-item {
  padding: 14px 12px;
  background: #ffffff;
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.stat-ring {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  flex-shrink: 0;
  position: relative;
  background: #e5e5e5;
}

.stat-ring::after {
  content: '';
  position: absolute;
  top: 6px;
  right: 6px;
  bottom: 6px;
  left: 6px;
  border-radius: 50%;
  background: #ffffff;
}

.stat-ring-total { background: conic-gradient(#94a3b8 0% 100%); }
.stat-ring-pending { background: conic-gradient(#64748b 0% 32%, #e5e5e5 32% 100%); }
.stat-ring-producing { background: conic-gradient(#475569 0% 18%, #e5e5e5 18% 100%); }
.stat-ring-done { background: conic-gradient(#334155 0% 50%, #e5e5e5 50% 100%); }

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-val {
  font-size: 18px;
  font-weight: 600;
  display: block;
  letter-spacing: -0.02em;
}

.stat-lab {
  font-size: 10px;
  color: #999999;
  margin-top: 2px;
  display: block;
}

.panel {
  display: none;
  padding: 24px;
}

.panel.is-active {
  display: block;
}

.dashboard-intro {
  font-size: 12px;
  color: #999999;
  margin-bottom: 20px;
}

.dashboard-sections {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.section-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  margin-bottom: 12px;
}

.section-title {
  font-size: 15px;
  font-weight: 600;
  margin-bottom: 4px;
}

.section-sub {
  font-size: 12px;
  color: #999999;
}

.section-link {
  border: none;
  background: none;
  padding: 4px 0;
  font-size: 12px;
  color: #999999;
  cursor: pointer;
}

.section-link:hover {
  color: #000000;
}

.search-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 14px;
}

.search-wrap {
  position: relative;
  flex: 1;
  max-width: 360px;
}

.search-wrap svg {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  width: 16px;
  height: 16px;
  color: #999999;
  stroke-width: 1.5;
  pointer-events: none;
}

.search-input {
  width: 100%;
  padding: 9px 12px 9px 36px;
  border: 1px solid #e5e5e5;
  border-radius: 999px;
  font-size: 13px;
  background: #fafafa;
  outline: none;
  transition: border-color 0.15s, background 0.15s;
}

.search-input:focus {
  background: #fff;
  border-color: #bbb;
}

.search-input::placeholder {
  color: #999999;
}

.table-wrap {
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.06);
  overflow: hidden;
  background: #ffffff;
}

.table-scroll {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  min-width: 800px;
}

th, td {
  padding: 10px 12px;
  text-align: left;
  font-size: 12px;
  border-bottom: 1px solid #f0f0f0;
}

th {
  font-weight: 500;
  color: #999999;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  font-size: 11px;
  background: #fafafa;
}

tbody tr:hover {
  background: #fafafa;
}

.cell-muted {
  color: #666666;
}

.btn-icon {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 5px 8px;
  font-size: 11px;
  color: #000000;
  background: transparent;
  border: 1px solid transparent;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.15s, border-color 0.15s;
}

.btn-icon svg {
  width: 14px;
  height: 14px;
  stroke-width: 1.5;
  flex-shrink: 0;
}

.btn-icon:hover {
  background: #f5f5f5;
  border-color: #e5e5e5;
}

.btn-ghost {
  padding: 5px 10px;
  font-size: 11px;
  color: #000000;
  background: #f5f5f5;
  border: 1px solid #e5e5e5;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.15s;
}

.btn-ghost:hover {
  background: #ebebeb;
}

.btn-ghost.danger {
  color: #666666;
}

.btn-ghost.danger:hover {
  background: #f0f0f0;
  color: #000000;
}

.badge {
  display: inline-flex;
  align-items: center;
  padding: 3px 8px;
  border-radius: 999px;
  font-size: 10px;
  font-weight: 500;
  white-space: nowrap;
}

.badge-new {
  background: #f5f5f5;
  border: 1px solid #e0e0e0;
  color: #000000;
}

.badge-pending {
  background: #ebebeb;
  border: 1px solid #d0d0d0;
  color: #000000;
}

.badge-producing {
  background: #d8d8d8;
  border: 1px solid #b8b8b8;
  color: #000000;
}

.badge-done {
  background: #333333;
  border: 1px solid #333333;
  color: #ffffff;
}

.progress-wrap {
  min-width: 80px;
}

.progress-bar {
  height: 5px;
  border-radius: 999px;
  background: #eee;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: inherit;
  background: #000000;
  transition: width 0.2s;
}

.progress-label {
  font-size: 10px;
  color: #999999;
  margin-top: 3px;
}

.template-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 16px;
}

.template-card {
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  padding: 16px 18px;
  background: #ffffff;
  box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}

.template-card h4 {
  font-size: 13px;
  font-weight: 600;
  margin: 0 0 6px 0;
}

.template-card p {
  font-size: 11px;
  color: #666666;
  margin: 0 0 12px 0;
}

@media (max-width: 1024px) {
  .main-wrapper {
    flex-direction: column;
  }
  .left-sider {
    width: 100%;
    flex-direction: row;
    overflow-x: auto;
  }
  .nav-card {
    min-width: 200px;
  }
  .mini-stats {
    min-width: 200px;
  }
}
</style>
