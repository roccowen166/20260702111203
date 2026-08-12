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

    <div v-loading="loading" class="card-grid">
      <el-card v-for="row in issues" :key="row.id" class="record-card" shadow="hover">
        <div class="flex items-start justify-between gap-3 mb-3"><h3 class="font-semibold truncate">{{ row.title }}</h3><div class="flex gap-1"><el-tag :type="severityType(row.severity)">{{ severityLabel(row.severity) }}</el-tag><el-tag :type="statusType(row.status)">{{ statusLabel(row.status) }}</el-tag></div></div>
        <div class="text-sm text-gray-500 line-clamp-2 mb-3">{{ row.description || '暂无描述' }}</div>
        <div class="grid grid-cols-2 gap-2 text-xs text-gray-500 mb-4"><span>项目：{{ projects.find(p => p.id === row.project_id)?.name || '-' }}</span><span>报告人：{{ row.reporter || '-' }}</span><span>负责人：{{ row.assignee || '-' }}</span><span>{{ row.created_at }}</span></div>
        <div class="card-actions"><el-button size="small" @click="handleEdit(row)">编辑</el-button><el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button></div>
      </el-card>
    </div>
    <el-empty v-if="!loading && !issues.length" description="暂无问题记录" />
    <el-card shadow="never" v-if="issues.length">
      <div class="flex justify-end mt-4">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.pageSize"
          :total="pagination.total"
          :page-sizes="[10, 20, 50]"
          layout="total, sizes, prev, pager, next"
          @size-change="loadData"
          @current-change="loadData"
        />
      </div>
    </el-card>

    <!-- 新建/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑问题' : '新建问题'"
      width="600px"
      @closed="resetForm"
    >
      <el-form ref="formRef" :model="form" :rules="rules" label-width="90px">
        <el-form-item label="项目" prop="project_id">
          <el-select v-model="form.project_id" placeholder="请选择项目" style="width: 100%">
            <el-option v-for="p in projects" :key="p.id" :label="p.name" :value="p.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="标题" prop="title">
          <el-input v-model="form.title" placeholder="请输入问题标题" maxlength="200" show-word-limit />
        </el-form-item>
        <el-form-item label="严重程度" prop="severity">
          <el-select v-model="form.severity" style="width: 100%">
            <el-option label="低" value="low" />
            <el-option label="中" value="medium" />
            <el-option label="高" value="high" />
            <el-option label="严重" value="critical" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="form.status" style="width: 100%">
            <el-option label="待处理" value="open" />
            <el-option label="处理中" value="in_progress" />
            <el-option label="已解决" value="resolved" />
            <el-option label="已关闭" value="closed" />
          </el-select>
        </el-form-item>
        <el-form-item label="报告人" prop="reporter">
          <el-input v-model="form.reporter" placeholder="请输入报告人" />
        </el-form-item>
        <el-form-item label="负责人" prop="assignee">
          <el-input v-model="form.assignee" placeholder="请输入负责人" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="4"
            placeholder="请输入问题描述"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { issueApi, type Issue } from '@/api/issue'
import { projectApi, type Project } from '@/api/project'

const issues = ref<Issue[]>([])
const projects = ref<Project[]>([])
const loading = ref(false)
const submitting = ref(false)
const dialogVisible = ref(false)
const isEdit = ref(false)
const editingId = ref<number | null>(null)
const formRef = ref<FormInstance>()

const filters = reactive({
  projectId: undefined as number | undefined,
  status: '',
  severity: '',
})

const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0,
})

const form = reactive({
  project_id: undefined as number | undefined,
  title: '',
  description: '',
  severity: 'medium',
  status: 'open',
  reporter: '',
  assignee: '',
})

const rules: FormRules = {
  project_id: [{ required: true, message: '请选择项目', trigger: 'change' }],
  title: [{ required: true, message: '请输入问题标题', trigger: 'blur' }],
  severity: [{ required: true, message: '请选择严重程度', trigger: 'change' }],
  status: [{ required: true, message: '请选择状态', trigger: 'change' }],
}

async function loadData() {
  loading.value = true
  try {
    const res = await issueApi.list({
      page: pagination.page,
      pageSize: pagination.pageSize,
      ...filters,
    })
    issues.value = res.items || res
    pagination.total = res.total ?? (res.items || res).length
  } finally {
    loading.value = false
  }
}

async function loadProjects() {
  const res = await projectApi.list({ pageSize: 100 })
  projects.value = res.items || res
}

function severityType(s: string): any {
  const map: Record<string, string> = { low: 'info', medium: '', high: 'warning', critical: 'danger' }
  return map[s] || ''
}

function severityLabel(s: string) {
  const map: Record<string, string> = { low: '低', medium: '中', high: '高', critical: '严重' }
  return map[s] || s
}

function statusType(s: string): any {
  const map: Record<string, string> = { open: 'danger', in_progress: 'warning', resolved: 'success', closed: 'info' }
  return map[s] || ''
}

function statusLabel(s: string) {
  const map: Record<string, string> = { open: '待处理', in_progress: '处理中', resolved: '已解决', closed: '已关闭' }
  return map[s] || s
}

function resetForm() {
  formRef.value?.resetFields()
  form.project_id = undefined
  form.title = ''
  form.description = ''
  form.severity = 'medium'
  form.status = 'open'
  form.reporter = ''
  form.assignee = ''
  isEdit.value = false
  editingId.value = null
}

function handleCreate() {
  resetForm()
  if (filters.projectId) {
    form.project_id = filters.projectId
  }
  dialogVisible.value = true
}

function handleEdit(row: Issue) {
  resetForm()
  isEdit.value = true
  editingId.value = row.id
  form.project_id = row.project_id
  form.title = row.title
  form.description = row.description || ''
  form.severity = row.severity
  form.status = row.status
  form.reporter = row.reporter || ''
  form.assignee = row.assignee || ''
  dialogVisible.value = true
}

async function handleSubmit() {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (!valid) return
    submitting.value = true
    try {
      const payload = {
        project_id: form.project_id!,
        title: form.title,
        description: form.description,
        severity: form.severity as Issue['severity'],
        status: form.status as Issue['status'],
        reporter: form.reporter,
        assignee: form.assignee,
      }
      if (isEdit.value && editingId.value) {
        await issueApi.update(editingId.value, payload)
        ElMessage.success('更新成功')
      } else {
        await issueApi.create(payload)
        ElMessage.success('创建成功')
      }
      dialogVisible.value = false
      loadData()
    } catch (err: any) {
      ElMessage.error(err?.response?.data?.detail || '操作失败')
    } finally {
      submitting.value = false
    }
  })
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
