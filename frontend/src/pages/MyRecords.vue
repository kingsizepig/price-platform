<template>
  <div class="my-records">
    <van-list
      v-model:loading="loading"
      :finished="finished"
      finished-text="没有更多了"
      @load="loadData"
    >
      <van-card
        v-for="item in list"
        :key="item.id"
        :title="item.product_name"
        :desc="item.create_time.slice(0, 10)"
      >
        <div class="price-row">
          <span class="price">¥{{ item.price }}</span>
          <van-button size="small" @click="editItem(item)">编辑</van-button>
        </div>
      </van-card>
    </van-list>

    <van-empty v-if="list.length === 0 && !loading" description="还没有录入价格" />

    <!-- 编辑弹窗 -->
    <van-popup v-model:show="showEdit" position="bottom">
      <van-form @submit="onSubmitEdit">
        <van-field
          v-model="editForm.price"
          name="price"
          label="价格"
          type="number"
        />
        <van-field
          v-model="editForm.location"
          name="location"
          label="所在地"
        />
        <div style="padding: 10px;">
          <van-button block type="primary" native-type="submit">保存</van-button>
          <van-button block @click="showEdit = false">取消</van-button>
        </div>
      </van-form>
    </van-popup>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../utils/api'
import { showToast } from 'vant'

const router = useRouter()
const list = ref([])
const loading = ref(false)
const finished = ref(false)
const showEdit = ref(false)
const editingId = ref(null)
const editForm = ref({
  price: '',
  location: '',
})

const loadData = async () => {
  loading.value = true
  try {
    const res = await api.listMyPrices(page.value, 20)
    if (res.data.code === 0) {
      list.value = res.data.data.list
      finished.value = !res.data.data.list.length || res.data.data.list.length < 20
    }
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const editItem = (item) => {
  editingId.value = item.id
  editForm.value = {
    price: item.price,
    location: item.location || '',
  }
  showEdit.value = true
}

const onSubmitEdit = async () => {
  try {
    await api.updatePrice(editingId.value, editForm.value)
    showToast('修改成功')
    showEdit.value = false
    loadData()
  } catch (e) {
    showToast('修改失败')
  }
}

onMounted(() => {
  loadData()
})
</script>

<style lang="less" scoped>
.my-records {
  min-height: 100vh;
  background: #f7f8fa;
  
  .price-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    
    .price {
      color: #ee0a24;
      font-weight: bold;
      font-size: 18px;
    }
  }
}
</style>
