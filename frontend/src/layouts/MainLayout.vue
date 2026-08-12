<template>
  <el-container class="app-shell h-screen">
    <!-- 侧边栏 -->
    <el-aside :width="isCollapse ? '68px' : '228px'" class="app-sidebar transition-all duration-300">
      <div class="logo-area flex items-center justify-center h-16">
        <el-icon v-if="isCollapse" :size="24" color="#a9c3ff"><Setting /></el-icon>
        <span v-else class="brand-lockup"><span class="brand-mark">T</span>测试流程系统</span>
      </div>
      <el-menu
        :default-active="activeMenu"
        :collapse="isCollapse"
        router
        background-color="transparent"
        text-color="#b8c4da"
        active-text-color="#ffffff"
        class="app-menu !border-r-0"
      >
        <el-menu-item index="/projects">
          <el-icon><Folder /></el-icon>
          <template #title>项目管理</template>
        </el-menu-item>
        <el-menu-item index="/issues">
          <el-icon><Warning /></el-icon>
          <template #title>问题记录</template>
        </el-menu-item>
        <el-menu-item index="/test-cases">
          <el-icon><Document /></el-icon>
          <template #title>测试用例</template>
        </el-menu-item>
        <el-menu-item index="/reports">
          <el-icon><Download /></el-icon>
          <template #title>报表导出</template>
        </el-menu-item>
        <el-menu-item v-if="userStore.isAdmin" index="/users">
          <el-icon><User /></el-icon>
          <template #title>用户管理</template>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-container>
      <!-- 顶部导航 -->
      <el-header class="app-header flex items-center justify-between border-b bg-white">
        <div class="flex items-center gap-3">
          <el-icon
            class="menu-toggle cursor-pointer text-xl"
            @click="isCollapse = !isCollapse"
          >
            <Fold v-if="!isCollapse" />
            <Expand v-else />
          </el-icon>
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>{{ currentTitle }}</el-breadcrumb-item>
          </el-breadcrumb>
        </div>

        <el-dropdown @command="handleCommand">
          <span class="flex items-center gap-2 cursor-pointer">
            <el-avatar :size="32" :icon="UserFilled" />
            <span class="user-name text-sm">{{ userStore.userInfo?.full_name }}</span>
            <el-tag class="role-tag" :type="userStore.isAdmin ? 'danger' : 'info'" size="small">
              {{ userStore.isAdmin ? '管理员' : '测试员' }}
            </el-tag>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="logout">
                <el-icon><SwitchButton /></el-icon>
                退出登录
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </el-header>

      <!-- 主内容区 -->
      <el-main>
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { UserFilled } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const isCollapse = ref(false)
const activeMenu = computed(() => '/' + (route.path.split('/')[1] || ''))
const currentTitle = computed(() => (route.meta.title as string) || '')

function handleCommand(command: string) {
  if (command === 'logout') {
    userStore.logout()
    router.push('/login')
  }
}
</script>

<style scoped>
.logo-area {
  background: linear-gradient(145deg, #172540 0%, #20335b 100%);
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.app-shell {
  background: #f4f7fb;
}

.app-sidebar {
  overflow: hidden;
  background: #172540;
  color: #fff;
}

.brand-lockup {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  color: #fff;
  font-size: 16px;
  font-weight: 700;
  letter-spacing: -0.02em;
  white-space: nowrap;
}

.brand-mark {
  display: inline-grid;
  width: 30px;
  height: 30px;
  place-items: center;
  border-radius: 9px;
  background: #5d87e8;
  color: #fff;
  font-size: 17px;
  font-weight: 800;
}

.app-menu {
  padding: 14px 10px;
}

.app-menu :deep(.el-menu-item) {
  height: 46px;
  margin: 4px 0;
  border-radius: 10px;
  color: #b8c4da;
}

.app-menu :deep(.el-menu-item:hover) {
  background: rgba(255, 255, 255, 0.08);
  color: #fff;
}

.app-menu :deep(.el-menu-item.is-active) {
  background: #3568d4;
  box-shadow: 0 8px 18px rgba(53, 104, 212, 0.3);
  color: #fff;
}

.app-header {
  height: 64px;
  padding: 0 28px;
  border-color: #e8edf4;
  box-shadow: 0 1px 0 rgba(31, 49, 83, 0.02);
}

.menu-toggle {
  color: #63708a;
}

.menu-toggle:hover {
  color: #3568d4;
}

.user-name {
  color: #2b3650;
  font-weight: 600;
}

.role-tag {
  border: 0;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@media (max-width: 680px) {
  .app-header {
    padding: 0 14px;
  }

  .user-name {
    display: none;
  }
}
</style>
