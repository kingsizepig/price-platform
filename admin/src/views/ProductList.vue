<template>
  <div class="product-list">
    <el-card>
      <div class="toolbar">
        <el-button type="primary" @click="handleAdd">添加商品</el-button>
      </div>
      <el-table :data="list" v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="商品名称" min-width="200" />
        <el-table-column prop="category_name" label="分类" width="120" />
        <el-table-column prop="price_count" label="价格记录数" width="120" align="center">
          <template #default="{ row }">
            {{ row.price_count || 0 }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" align="center">
          <template #default="{ row }">
            <el-button size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
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

    <!-- 编辑弹窗 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="500px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="商品名称" required>
          <el-input v-model="form.name" placeholder="请输入商品名称" />
        </el-form-item>
        <el-form-item label="商品条码">
          <el-input v-model="form.barcode" placeholder="请输入条码" />
        </el-form-item>
        <el-form-item label="分类">
          <el-select v-model="form.category_id" placeholder="请选择分类" clearable>
            <el-option v-for="item in categories" :key="item.id" :label="item.name" :value="item.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" placeholder="商品描述" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { productApi, categoryApi } from '../utils/api'

const loading = ref(false)
const list = ref([])
const categories = ref([])
const dialogVisible = ref(false)
const dialogTitle = ref('添加商品')
const pagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0
})
const form = reactive({
  id: null,
  name: '',
  barcode: '',
  category_id: null,
  description: ''
})

const loadData = async () => {
  loading.value = true
  try {
    const res = await productApi.list({
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

const loadCategories = async () => {
  try {
    const res = await categoryApi.list()
    categories.value = res || []
  } catch (e) {
    console.error(e)
  }
}

const handleAdd = () => {
  Object.assign(form, {
    id: null,
    name: '',
    barcode: '',
    category_id: null,
    description: ''
  })
  dialogTitle.value = '添加商品'
  dialogVisible.value = true
}

const handleEdit = (row) => {
  Object.assign(form, { ...row })
  dialogTitle.value = '编辑商品'
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (!form.name) {
    ElMessage.warning('请输入商品名称')
    return
  }
  try {
    if (form.id) {
      await productApi.update(form.id, form)
      ElMessage.success('更新成功')
    } else {
      await productApi.create(form)
      ElMessage.success('添加成功')
    }
    dialogVisible.value = false
    loadData()
  } catch (e) {
    console.error(e)
  }
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除这个商品吗？删除后不可恢复', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await productApi.delete(row.id)
    ElMessage.success('删除成功')
    loadData()
  } catch (e) {
    if (e !== 'cancel') {
      console.error(e)
    }
  }
}

onMounted(() => {
  loadData()
  loadCategories()
})
</script>

<style scoped>
.product-list {
  padding: 20px 0;
}

.toolbar {
  margin-bottom: 16px;
}
</style>
