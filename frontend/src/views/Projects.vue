<template>
  <div class="p-4">
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-xl font-bold">项目管理</h2>
      <el-button type="primary" :icon="Plus" @click="handleCreate">新建项目</el-button>
    </div>

    <el-card shadow="never">
      <el-table :data="projects" v-loading="loading" stripe>
        <el-table-column prop="name" label="项目名称" min-width="180" />
        <el-table-column prop="description" label="描述" min-width="200" show-overflow-tooltip />
        <el-table-column prop="status" label="状态" width="120">
          <template #default="{ row }">
            <el-tag :type="statusType(row.status)">{{ statusLabel(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column label="操作" width="240" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="goDetail(row.id)">进入</el-button>
            <el-button size="small" type="primary" @click="handleEdit(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Plus } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { projectApi, type Project } from '@/api/project'

const router = useRouter()
const projects = ref<Project[]>([])
const loading = ref(false)

async function loadData() {
  loading.value = true
  try {
    const res = await projectApi.list({ page: 1, pageSize: 100 })
    projects.value = res.items || res
  } finally {
    loading.value = false
  }
}

function statusType(status: string) {
  const map: Record<string, string> = { active: 'success', archived: 'info', draft: 'warning' }
  return map[status] || ''
}

function statusLabel(status: string) {
  const map: Record<string, string> = { active: '进行中', archived: '已归档', draft: '草稿' }
  return map[status] || status
}

function goDetail(id: number) {
  router.push(`/projects/${id}`)
}

function handleCreate() {
  ElMessage.info('新建项目功能开发中...')
}

function handleEdit(_row: Project) {
  ElMessage.info('编辑功能开发中...')
}

async function handleDelete(row: Project) {
  await ElMessageBox.confirm(`确认删除项目「${row.name}」？`, '提示', { type: 'warning' })
  await projectApi.delete(row.id)
  ElMessage.success('删除成功')
  loadData()
}

onMounted(loadData)
</script>
