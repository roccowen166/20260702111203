<template>
  <div class="flex flex-col items-center justify-center min-h-screen">
    <el-result icon="error" title="404" sub-title="抱歉，页面不存在">
      <template #extra>
        <el-button type="primary" @click="$router.push('/')">返回首页</el-button>
      </template>
    </el-result>
  </div>
</template>
