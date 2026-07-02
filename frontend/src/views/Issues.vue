<template>
  <div class="p-4">
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-xl font-bold">问题记录</h2>
      <el-button type="primary" :icon="Plus" @click="handleCreate">新建问题</el-button>
    </div>

    <el-card shadow="never" class="mb-4">
      <el-form inline>
        <el-form-item label="项目">
          <el-select v-model="filters.projectId" placeholder="全部" clearable style="width: 160px">
            <el-option v-for="p in projects" :key="p.id" :label="p.name" :value="p.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="filters.status" placeholder="全部" clearable style="width: 120px">
            <el-option label="待处理" value="open" />
            <el-option label="处理中" value="in_progress" />
            <el-option label="已解决" value="resolved" />
            <el-option label="已关闭" value="closed" />
          </el-select>
        </el-form-item>
        <el-form-item label="严重程度">
          <el-select v-model="filters.severity" placeholder="全部" clearable style="width: 120px">
            <el-option label="低" value="low" />
            <el-option label="中" value="medium" />
            <el-option label="高" value="high" />
            <el-option label="严重" value="critical" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadData">查询</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card shadow="never">
      <el-table :data="issues" v-loading="loading" stripe>
        <el-table-column prop="title" label="标题" min-width="200" show-overflow-tooltip />
        <el-table-column prop="severity" label="严重程度" width="100">
          <template #default="{ row }">
            <el-tag :type="severityType(row.severity)">{{ severityLabel(row.severity) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="statusType(row.status)">{{ statusLabel(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="reporter" label="报告人" width="120" />
        <el-table-column prop="assignee" label="负责人" width="120" />
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { issueApi, type Issue } from '@/api/issue'
import { projectApi, type Project } from '@/api/project'

const issues = ref<Issue[]>([])
const projects = ref<Project[]>([])
const loading = ref(false)

const filters = reactive({
  projectId: undefined as number | undefined,
  status: '',
  severity: '',
})

async function loadData() {
  loading.value = true
  try {
    const res = await issueApi.list(filters)
    issues.value = res.items || res
  } finally {
    loading.value = false
  }
}

async function loadProjects() {
  const res = await projectApi.list({ pageSize: 100 })
  projects.value = res.items || res
}

function severityType(s: string) {
  const map: Record<string, string> = { low: 'info', medium: '', high: 'warning', critical: 'danger' }
  return map[s] || ''
}

function severityLabel(s: string) {
  const map: Record<string, string> = { low: '低', medium: '中', high: '高', critical: '严重' }
  return map[s] || s
}

function statusType(s: string) {
  const map: Record<string, string> = { open: 'danger', in_progress: 'warning', resolved: 'success', closed: 'info' }
  return map[s] || ''
}

function statusLabel(s: string) {
  const map: Record<string, string> = { open: '待处理', in_progress: '处理中', resolved: '已解决', closed: '已关闭' }
  return map[s] || s
}

function handleCreate() {
  ElMessage.info('新建问题功能开发中...')
}

function handleEdit(_row: Issue) {
  ElMessage.info('编辑功能开发中...')
}

async function handleDelete(row: Issue) {
  await ElMessageBox.confirm(`确认删除问题「${row.title}」？`, '提示', { type: 'warning' })
  await issueApi.delete(row.id)
  ElMessage.success('删除成功')
  loadData()
}

onMounted(() => {
  loadProjects()
  loadData()
})
</script>
