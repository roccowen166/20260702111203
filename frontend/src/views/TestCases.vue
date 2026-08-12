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

    <div v-loading="loading" class="card-grid">
      <el-card v-for="row in testCases" :key="row.id" class="record-card" shadow="hover">
        <div class="flex items-start justify-between gap-3 mb-3"><h3 class="font-semibold truncate">{{ row.title }}</h3><div class="flex gap-1"><el-tag :type="priorityType(row.priority)">{{ priorityLabel(row.priority) }}</el-tag><el-tag :type="statusType(row.status)">{{ statusLabel(row.status) }}</el-tag></div></div>
        <div class="text-sm text-gray-500 line-clamp-2 mb-3">{{ row.description || '暂无描述' }}</div>
        <div class="grid grid-cols-2 gap-2 text-xs text-gray-500 mb-4"><span>项目：{{ projects.find(p => p.id === row.project_id)?.name || '-' }}</span><span>步骤：{{ row.steps?.length || 0 }}</span><span>创建人：{{ row.created_by_name || row.created_by || '-' }}</span><span>{{ row.created_at }}</span></div>
        <div class="card-actions"><el-button size="small" @click="handleEdit(row)">编辑</el-button><el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button></div>
      </el-card>
    </div>
    <el-empty v-if="!loading && !testCases.length" description="暂无测试用例" />
    <!-- 新建/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑用例' : '新建用例'"
      width="720px"
      @closed="resetForm"
    >
      <el-form ref="formRef" :model="form" :rules="rules" label-width="90px">
        <el-form-item label="项目" prop="project_id">
          <el-select v-model="form.project_id" placeholder="请选择项目" style="width: 100%">
            <el-option v-for="p in projects" :key="p.id" :label="p.name" :value="p.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="用例标题" prop="title">
          <el-input v-model="form.title" placeholder="请输入用例标题" maxlength="200" show-word-limit />
        </el-form-item>
        <el-form-item label="优先级" prop="priority">
          <el-select v-model="form.priority" style="width: 100%">
            <el-option label="低" value="low" />
            <el-option label="中" value="medium" />
            <el-option label="高" value="high" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="form.status" style="width: 100%">
            <el-option label="草稿" value="draft" />
            <el-option label="启用" value="active" />
            <el-option label="废弃" value="deprecated" />
          </el-select>
        </el-form-item>
        <el-form-item label="前置条件" prop="preconditions">
          <el-input
            v-model="form.preconditions"
            type="textarea"
            :rows="2"
            placeholder="请输入前置条件"
          />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="2"
            placeholder="请输入用例描述"
          />
        </el-form-item>
        <el-form-item label="测试步骤">
          <div class="w-full">
            <div
              v-for="(step, index) in form.steps"
              :key="index"
              class="flex items-start gap-2 mb-2"
            >
              <el-tag type="info" class="mt-1.5">{{ index + 1 }}</el-tag>
              <el-input
                v-model="step.action"
                placeholder="操作步骤"
                style="flex: 1"
              />
              <el-input
                v-model="step.expected_result"
                placeholder="预期结果"
                style="flex: 1"
              />
              <el-button
                type="danger"
                :icon="Delete"
                circle
                class="mt-1"
                @click="removeStep(index)"
              />
            </div>
            <el-button type="primary" plain :icon="Plus" @click="addStep">添加步骤</el-button>
          </div>
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
import { Plus, Delete } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { testCaseApi, type TestCase, type TestCaseStep } from '@/api/testCase'
import { projectApi, type Project } from '@/api/project'

const testCases = ref<TestCase[]>([])
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
})

const form = reactive({
  project_id: undefined as number | undefined,
  title: '',
  description: '',
  preconditions: '',
  steps: [] as TestCaseStep[],
  priority: 'medium',
  status: 'draft',
})

const rules: FormRules = {
  project_id: [{ required: true, message: '请选择项目', trigger: 'change' }],
  title: [{ required: true, message: '请输入用例标题', trigger: 'blur' }],
  priority: [{ required: true, message: '请选择优先级', trigger: 'change' }],
  status: [{ required: true, message: '请选择状态', trigger: 'change' }],
}

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

function priorityType(p: string): any {
  const map: Record<string, string> = { low: 'info', medium: '', high: 'danger' }
  return map[p] || ''
}

function priorityLabel(p: string) {
  const map: Record<string, string> = { low: '低', medium: '中', high: '高' }
  return map[p] || p
}

function statusType(s: string): any {
  const map: Record<string, string> = { draft: 'info', active: 'success', deprecated: 'danger' }
  return map[s] || ''
}

function statusLabel(s: string) {
  const map: Record<string, string> = { draft: '草稿', active: '启用', deprecated: '废弃' }
  return map[s] || s
}

function addStep() {
  form.steps.push({ step_no: form.steps.length + 1, action: '', expected_result: '' })
}

function removeStep(index: number) {
  form.steps.splice(index, 1)
  form.steps.forEach((s, i) => (s.step_no = i + 1))
}

function resetForm() {
  formRef.value?.resetFields()
  form.project_id = undefined
  form.title = ''
  form.description = ''
  form.preconditions = ''
  form.steps = []
  form.priority = 'medium'
  form.status = 'draft'
  isEdit.value = false
  editingId.value = null
}

function handleCreate() {
  resetForm()
  if (filters.projectId) {
    form.project_id = filters.projectId
  }
  addStep()
  dialogVisible.value = true
}

function handleEdit(row: TestCase) {
  resetForm()
  isEdit.value = true
  editingId.value = row.id
  form.project_id = row.project_id
  form.title = row.title
  form.description = row.description || ''
  form.preconditions = row.preconditions || ''
  form.steps = (row.steps || []).map((s) => ({ ...s }))
  form.priority = row.priority
  form.status = row.status
  if (form.steps.length === 0) addStep()
  dialogVisible.value = true
}

async function handleSubmit() {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (!valid) return
    submitting.value = true
    try {
      const steps = form.steps
        .filter((s) => s.action.trim())
        .map((s, i) => ({
          step_no: i + 1,
          action: s.action,
          expected_result: s.expected_result,
        }))
      const payload = {
        project_id: form.project_id!,
        title: form.title,
        description: form.description,
        preconditions: form.preconditions,
        steps,
        priority: form.priority as TestCase['priority'],
        status: form.status as TestCase['status'],
      }
      if (isEdit.value && editingId.value) {
        await testCaseApi.update(editingId.value, payload)
        ElMessage.success('更新成功')
      } else {
        await testCaseApi.create(payload)
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
