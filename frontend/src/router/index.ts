import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/Login.vue'),
      meta: { title: '登录', requiresAuth: false },
    },
    {
      path: '/',
      component: () => import('@/layouts/MainLayout.vue'),
      meta: { requiresAuth: true },
      redirect: '/projects',
      children: [
        {
          path: 'projects',
          name: 'Projects',
          component: () => import('@/views/Projects.vue'),
          meta: { title: '项目管理', icon: 'Folder' },
        },
        {
          path: 'projects/:id',
          name: 'ProjectDetail',
          component: () => import('@/views/ProjectDetail.vue'),
          meta: { title: '项目详情', hidden: true },
        },
        {
          path: 'issues',
          name: 'Issues',
          component: () => import('@/views/Issues.vue'),
          meta: { title: '问题记录', icon: 'Warning' },
        },
        {
          path: 'test-cases',
          name: 'TestCases',
          component: () => import('@/views/TestCases.vue'),
          meta: { title: '测试用例', icon: 'Document' },
        },
        {
          path: 'reports',
          name: 'Reports',
          component: () => import('@/views/Reports.vue'),
          meta: { title: '报表导出', icon: 'Download' },
        },
        {
          path: 'users',
          name: 'Users',
          component: () => import('@/views/Users.vue'),
          meta: { title: '用户管理', icon: 'User', requiresAdmin: true },
        },
      ],
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: () => import('@/views/NotFound.vue'),
    },
  ],
})

// 路由守卫
router.beforeEach((to, _from, next) => {
  const userStore = useUserStore()
  const token = userStore.token

  if (to.meta.title) {
    document.title = `${to.meta.title} - 标准测试流程系统`
  }

  if (to.meta.requiresAuth === false) {
    // 已登录用户访问登录页，重定向到首页
    if (token && to.name === 'Login') {
      next({ path: '/' })
    } else {
      next()
    }
    return
  }

  // 需要认证但未登录
  if (!token) {
    next({ path: '/login', query: { redirect: to.fullPath } })
    return
  }

  // 需要管理员权限
  if (to.meta.requiresAdmin && userStore.role !== 'admin') {
    next({ path: '/' })
    return
  }

  next()
})

export default router
