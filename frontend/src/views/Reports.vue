<template>
  <div class="p-4">
    <h2 class="text-xl font-bold mb-6">报表导出</h2>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <el-card shadow="hover" class="text-center cursor-pointer" @click="exportIssues">
        <el-icon :size="48" color="#f56c6c" class="mb-4"><Warning /></el-icon>
        <h3 class="text-lg font-bold mb-2">问题记录报表</h3>
        <p class="text-gray-500 text-sm mb-4">按项目分Sheet导出问题记录</p>
        <el-button type="danger" :icon="Download" :loading="exporting === 'issues'">导出 Excel</el-button>
      </el-card>

      <el-card shadow="hover" class="text-center cursor-pointer" @click="exportTestCases">
        <el-icon :size="48" color="#409eff" class="mb-4"><Document /></el-icon>
        <h3 class="text-lg font-bold mb-2">测试用例报表</h3>
        <p class="text-gray-500 text-sm mb-4">导出所有测试用例为 Excel</p>
        <el-button type="primary" :icon="Download" :loading="exporting === 'cases'">导出 Excel</el-button>
      </el-card>

      <el-card shadow="hover" class="text-center cursor-pointer" @click="exportAll">
        <el-icon :size="48" color="#67c23a" class="mb-4"><Files /></el-icon>
        <h3 class="text-lg font-bold mb-2">汇总报表</h3>
        <p class="text-gray-500 text-sm mb-4">问题+用例汇总导出</p>
        <el-button type="success" :icon="Download" :loading="exporting === 'all'">导出 Excel</el-button>
      </el-card>
    </div>

    <el-card shadow="never" class="mt-6">
      <template #header><span class="font-bold">导出选项</span></template>
      <el-form inline label-width="80px">
        <el-form-item label="项目">
          <el-select v-model="filters.projectId" placeholder="全部项目" clearable style="width: 200px">
            <el-option v-for="p in projects" :key="p.id" :label="p.name" :value="p.id" />
          </el-select>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { Download, Warning, Document, Files } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { reportApi } from '@/api/report'
import { projectApi, type Project } from '@/api/project'

const exporting = ref('')
const projects = ref<Project[]>([])
const filters = reactive({ projectId: undefined as number | undefined })

async function loadProjects() {
  const res = await projectApi.list({ pageSize: 100 })
  projects.value = res.items || res
}

function downloadBlob(blob: Blob, filename: string) {
  const url = window.URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  a.click()
  window.URL.revokeObjectURL(url)
}

async function exportIssues() {
  exporting.value = 'issues'
  try {
    const blob = await reportApi.exportIssues(filters)
    const projectName = projects.value.find(p => p.id === filters.projectId)?.name || '全部项目'
    downloadBlob(blob as unknown as Blob, `问题记录报表_${projectName}_${Date.now()}.xlsx`)
    ElMessage.success('导出成功')
  } finally {
    exporting.value = ''
  }
}

async function exportTestCases() {
  exporting.value = 'cases'
  try {
    const blob = await reportApi.exportTestCases(filters)
    const projectName = projects.value.find(p => p.id === filters.projectId)?.name || '全部项目'
    downloadBlob(blob as unknown as Blob, `测试用例报表_${projectName}_${Date.now()}.xlsx`)
    ElMessage.success('导出成功')
  } finally {
    exporting.value = ''
  }
}

async function exportAll() {
  exporting.value = 'all'
  try {
    const blob = await reportApi.exportAll(filters)
    const projectName = projects.value.find(p => p.id === filters.projectId)?.name || '全部项目'
    downloadBlob(blob as unknown as Blob, `汇总报表_${projectName}_${Date.now()}.xlsx`)
    ElMessage.success('导出成功')
  } finally {
    exporting.value = ''
  }
}

onMounted(loadProjects)
</script>
