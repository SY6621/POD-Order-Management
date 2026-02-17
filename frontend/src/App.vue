<template>
  <div id="app">
    <!-- 生产订单管理系统使用独立布局 -->
    <template v-if="isProductionPage">
      <router-view />
    </template>
    
    <!-- 其他页面使用默认布局 -->
    <template v-else>
      <el-container>
        <el-aside width="200px" class="sidebar">
          <div class="logo">ETSY管理系统</div>
          <el-menu
            :default-active="$route.path"
            router
            background-color="#545c64"
            text-color="#fff"
            active-text-color="#ffd04b"
          >
            <el-menu-item index="/">
              <el-icon><Monitor /></el-icon>
              <span>仪表盘</span>
            </el-menu-item>
            <el-menu-item index="/orders">
              <el-icon><Document /></el-icon>
              <span>订单管理</span>
            </el-menu-item>
            <el-menu-item index="/effects">
              <el-icon><Picture /></el-icon>
              <span>效果图生成</span>
            </el-menu-item>
            <el-menu-item index="/production">
              <el-icon><Printer /></el-icon>
              <span>生产文档</span>
            </el-menu-item>
            <el-menu-item index="/logistics">
              <el-icon><Van /></el-icon>
              <span>物流管理</span>
            </el-menu-item>
            <el-menu-item index="/settings">
              <el-icon><Setting /></el-icon>
              <span>系统设置</span>
            </el-menu-item>
          </el-menu>
        </el-aside>
        <el-container>
          <el-header class="header">
            <h3>{{ $route.meta.title }}</h3>
            <div>
              <el-button type="primary" size="small">刷新邮件</el-button>
            </div>
          </el-header>
          <el-main>
            <router-view />
          </el-main>
        </el-container>
      </el-container>
    </template>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { Monitor, Document, Picture, Printer, Van, Setting } from '@element-plus/icons-vue'

const route = useRoute()

// 判断是否为使用独立布局的页面（Dashboard、生产订单管理）
const isProductionPage = computed(() => route.path === '/' || route.path === '/production')
</script>

<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
#app { height: 100vh; }
.sidebar { background-color: #545c64; height: 100vh; }
.logo { padding: 20px; color: white; font-weight: bold; text-align: center; font-size: 16px; }
.header { background-color: #fff; box-shadow: 0 1px 4px rgba(0,21,41,.08); display: flex; align-items: center; justify-content: space-between; padding: 0 20px; }
.header h3 { margin: 0; font-size: 18px; }
</style>
