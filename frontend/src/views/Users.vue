<template>
  <div class="p-4">
    <h2 class="text-xl font-bold mb-6">用户管理</h2>
    <div v-loading="loading" class="card-grid">
      <el-card v-for="row in users" :key="row.id || row.email" class="record-card" shadow="hover">
        <div class="flex items-center gap-3 mb-4"><el-avatar>{{ (row.full_name || row.email || '?').slice(0, 1).toUpperCase() }}</el-avatar><div><h3 class="font-semibold">{{ row.full_name || '未命名用户' }}</h3><p class="text-sm text-gray-500">{{ row.email }}</p></div></div>
        <div class="flex items-center justify-between"><el-tag :type="row.role === 'admin' ? 'danger' : 'info'">{{ row.role === 'admin' ? '管理员' : '测试员' }}</el-tag><span class="text-xs text-gray-400">{{ row.created_at }}</span></div>
      </el-card>
    </div>
    <el-empty v-if="!loading && !users.length" description="暂无用户" />
    <el-card shadow="never" style="display:none">
      <el-table :data="[]">
        <el-table-column prop="email" label="邮箱" min-width="200" />
        <el-table-column prop="full_name" label="姓名" width="150" />
        <el-table-column prop="role" label="角色" width="120">
          <template #default="{ row }">
            <el-tag :type="row.role === 'admin' ? 'danger' : 'info'">
              {{ row.role === 'admin' ? '管理员' : '测试员' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import request from '@/api/request'

const users = ref<any[]>([])
const loading = ref(false)

async function loadData() {
  loading.value = true
  try {
    const res = await request.get('/users')
    users.value = res.items || res
  } finally {
    loading.value = false
  }
}

onMounted(loadData)
</script>
