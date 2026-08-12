<template>
  <div class="p-4">
    <el-page-header @back="$router.back()" class="mb-4">
      <template #content>
        <span class="text-lg font-bold">{{ project?.name || '项目详情' }}</span>
      </template>
    </el-page-header>

    <!-- 项目信息 -->
    <el-card shadow="never" class="record-card mb-4">
      <el-descriptions :column="3" border>
        <el-descriptions-item label="项目名称">{{ project?.name }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag>{{ project?.status }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ project?.created_at }}</el-descriptions-item>
        <el-descriptions-item label="描述" :span="3">{{ project?.description }}</el-descriptions-item>
      </el-descriptions>
    </el-card>

    <!-- 原理图和图片 -->
    <el-card shadow="never">
      <template #header>
        <div class="flex items-center justify-between">
          <span class="font-bold">原理图与相关图片</span>
          <el-upload
            :show-file-list="false"
            :before-upload="handleUpload"
            accept="image/*,.pdf,.dwg"
          >
            <el-button type="primary" :icon="Upload">上传文件</el-button>
          </el-upload>
        </div>
      </template>

      <div v-loading="loading" class="card-grid">
        <el-card v-for="row in files" :key="row.id" class="record-card" shadow="hover">
          <div class="flex items-center gap-3 mb-3"><el-icon size="28" color="#409eff"><Document /></el-icon><div class="min-w-0"><div class="font-medium truncate">{{ row.filename }}</div><div class="text-xs text-gray-400">{{ row.file_type }} · {{ formatSize(row.file_size) }}</div></div></div>
          <div class="text-xs text-gray-400 mb-3">{{ row.uploaded_at }}</div>
          <div class="card-actions"><el-button size="small" type="primary" :icon="Download" @click="downloadFile(row)">下载</el-button><el-button size="small" type="danger" :icon="Delete" @click="deleteFile(row)">删除</el-button></div>
        </el-card>
      </div>
      <el-empty v-if="!loading && !files.length" description="暂无文件" />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { Upload, Download, Delete, Document } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { projectApi, type Project, type ProjectFile } from '@/api/project'

const route = useRoute()
const projectId = Number(route.params.id)

const project = ref<Project | null>(null)
const files = ref<ProjectFile[]>([])
const loading = ref(false)

async function loadProject() {
  project.value = await projectApi.detail(projectId)
}

async function loadFiles() {
  loading.value = true
  try {
    const res = await projectApi.files(projectId)
    files.value = res.items || res
  } finally {
    loading.value = false
  }
}

async function handleUpload(file: File) {
  await projectApi.uploadFile(projectId, file)
  ElMessage.success('上传成功')
  loadFiles()
  return false
}

function downloadFile(row: ProjectFile) {
  window.open(row.file_url, '_blank')
}

async function deleteFile(row: ProjectFile) {
  await ElMessageBox.confirm(`确认删除文件「${row.filename}」？`, '提示', { type: 'warning' })
  await projectApi.deleteFile(projectId, row.id)
  ElMessage.success('删除成功')
  loadFiles()
}

function formatSize(bytes: number) {
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / 1024 / 1024).toFixed(1) + ' MB'
}

onMounted(() => {
  loadProject()
  loadFiles()
})
</script>
