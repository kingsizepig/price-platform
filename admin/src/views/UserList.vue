<template>
  <div class="user-list">
    <el-card>
      <el-table :data="list" v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="username" label="用户名" width="150" />
        <el-table-column prop="nickname" label="昵称" width="150" />
        <el-table-column prop="level_name" label="等级" width="100" align="center" />
        <el-table-column prop="points" label="积分" width="100" align="center" />
        <el-table-column prop="created_at" label="注册时间" width="180" />
        <el-table-column label="操作" width="100" align="center">
          <template #default="{ row }">
            <el-button size="small" @click="handleEdit(row)">编辑</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        v-model:current-page="pagination.page"
        v-model:page-size="pagination.pageSize"
        @size-change="loadData"
        @current-change="loadData"
        :total="pagination.total"
        style="margin-top: 20px; justify-content: flex-end;"
        layout="total, sizes, prev, pager, next, jumper"
      />
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { userApi } from '../utils/api'

const loading = ref(false)
const list = ref([])
const pagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0
})

const loadData = async () => {
  loading.value = true
  try {
    const res = await userApi.list({
      page: pagination.page,
      page_size: pagination.pageSize
    })
    list.value = res.list || []
    pagination.total = res.total || 0
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const handleEdit = (row) => {
  // TODO: 编辑用户信息弹窗
  console.log('edit', row)
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.user-list {
  padding: 20px 0;
}
</style>
