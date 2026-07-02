<template>
  <div class="p-4">
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-xl font-bold">测试用例</h2>
      <el-button type="primary" :icon="Plus" @click="handleCreate">新建用例</el-button>
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
            <el-option label="草稿" value="draft" />
            <el-option label="启用" value="active" />
            <el-option label="废弃" value="deprecated" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadData">查询</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card shadow="never">
      <el-table :data="testCases" v-loading="loading" stripe>
        <el-table-column prop="title" label="用例标题" min-width="200" show-overflow-tooltip />
        <el-table-column prop="priority" label="优先级" width="100">
          <template #default="{ row }">
            <el-tag :type="priorityType(row.priority)">{{ priorityLabel(row.priority) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="statusType(row.status)">{{ statusLabel(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="步骤数" width="80">
          <template #default="{ row }">{{ row.steps?.length || 0 }}</template>
        </el-table-column>
        <el-table-column prop="created_by" label="创建人" width="120" />
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
import { testCaseApi, type TestCase } from '@/api/testCase'
import { projectApi, type Project } from '@/api/project'

const testCases = ref<TestCase[]>([])
const projects = ref<Project[]>([])
const loading = ref(false)

const filters = reactive({
  projectId: undefined as number | undefined,
  status: '',
})

async function loadData() {
  loading.value = true
  try {
    const res = await testCaseApi.list(filters)
    testCases.value = res.items || res
  } finally {
    loading.value = false
  }
}

async function loadProjects() {
  const res = await projectApi.list({ pageSize: 100 })
  projects.value = res.items || res
}

function priorityType(p: string) {
  const map: Record<string, string> = { low: 'info', medium: '', high: 'danger' }
  return map[p] || ''
}

function priorityLabel(p: string) {
  const map: Record<string, string> = { low: '低', medium: '中', high: '高' }
  return map[p] || p
}

function statusType(s: string) {
  const map: Record<string, string> = { draft: 'info', active: 'success', deprecated: 'danger' }
  return map[s] || ''
}

function statusLabel(s: string) {
  const map: Record<string, string> = { draft: '草稿', active: '启用', deprecated: '废弃' }
  return map[s] || s
}

function handleCreate() {
  ElMessage.info('新建用例功能开发中...')
}

function handleEdit(_row: TestCase) {
  ElMessage.info('编辑功能开发中...')
}

async function handleDelete(row: TestCase) {
  await ElMessageBox.confirm(`确认删除用例「${row.title}」？`, '提示', { type: 'warning' })
  await testCaseApi.delete(row.id)
  ElMessage.success('删除成功')
  loadData()
}

onMounted(() => {
  loadProjects()
  loadData()
})
</script>
