<template>
  <div class="p-4">
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-xl font-bold">项目管理</h2>
      <el-button type="primary" :icon="Plus" @click="handleCreate">新建项目</el-button>
    </div>

    <div class="metric-grid mb-6">
      <div class="metric-card"><span>项目总数</span><strong>{{ projects.length }}</strong></div>
      <div class="metric-card"><span>进行中</span><strong>{{ projects.filter(p => p.status === 'active').length }}</strong></div>
      <div class="metric-card"><span>已归档</span><strong>{{ projects.filter(p => p.status === 'archived').length }}</strong></div>
    </div>
    <div v-loading="loading" class="card-grid">
      <el-card v-for="row in projects" :key="row.id" class="record-card" shadow="hover">
        <div class="flex items-start justify-between gap-3 mb-3"><h3 class="text-lg font-semibold truncate">{{ row.name }}</h3><el-tag :type="statusType(row.status)">{{ statusLabel(row.status) }}</el-tag></div>
        <p class="text-gray-500 text-sm mb-4 line-clamp-2">{{ row.description || '暂无描述' }}</p>
        <div class="text-xs text-gray-400 mb-4">创建于 {{ row.created_at }}</div>
        <div class="card-actions"><el-button size="small" @click="goDetail(row.id)">进入</el-button><el-button size="small" type="primary" @click="handleEdit(row)">编辑</el-button><el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button></div>
      </el-card>
    </div>
    <el-empty v-if="!loading && !projects.length" description="暂无项目" />

    <!-- 新建/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑项目' : '新建项目'"
      width="560px"
      @closed="resetForm"
    >
      <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="项目名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入项目名称" maxlength="200" show-word-limit />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="form.status" style="width: 100%">
            <el-option label="进行中" value="active" />
            <el-option label="草稿" value="draft" />
            <el-option label="已归档" value="archived" />
          </el-select>
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="4"
            placeholder="请输入项目描述"
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
import { useRouter } from 'vue-router'
import { Plus } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { projectApi, type Project } from '@/api/project'

const router = useRouter()
const projects = ref<Project[]>([])
const loading = ref(false)
const submitting = ref(false)
const dialogVisible = ref(false)
const isEdit = ref(false)
const editingId = ref<number | null>(null)
const formRef = ref<FormInstance>()

const form = reactive({
  name: '',
  description: '',
  status: 'active',
})

const rules: FormRules = {
  name: [{ required: true, message: '请输入项目名称', trigger: 'blur' }],
  status: [{ required: true, message: '请选择状态', trigger: 'change' }],
}

async function loadData() {
  loading.value = true
  try {
    const res = await projectApi.list({ page: 1, pageSize: 100 })
    projects.value = res.items || res
  } finally {
    loading.value = false
  }
}

function statusType(status: string): any {
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

function resetForm() {
  formRef.value?.resetFields()
  form.name = ''
  form.description = ''
  form.status = 'active'
  isEdit.value = false
  editingId.value = null
}

function handleCreate() {
  resetForm()
  dialogVisible.value = true
}

function handleEdit(row: Project) {
  resetForm()
  isEdit.value = true
  editingId.value = row.id
  form.name = row.name
  form.description = row.description || ''
  form.status = row.status
  dialogVisible.value = true
}

async function handleSubmit() {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (!valid) return
    submitting.value = true
    try {
      const payload = {
        name: form.name,
        description: form.description,
        status: form.status,
      }
      if (isEdit.value && editingId.value) {
        await projectApi.update(editingId.value, payload)
        ElMessage.success('更新成功')
      } else {
        await projectApi.create(payload)
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

async function handleDelete(row: Project) {
  await ElMessageBox.confirm(`确认删除项目「${row.name}」？`, '提示', { type: 'warning' })
  await projectApi.delete(row.id)
  ElMessage.success('删除成功')
  loadData()
}

onMounted(loadData)
</script>
