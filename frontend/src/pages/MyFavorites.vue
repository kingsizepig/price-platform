<template>
  <div class="my-favorites">
    <van-list
      v-model:loading="loading"
      :finished="finished"
      finished-text="没有更多了"
      @load="loadData"
    >
      <van-cell
        v-for="item in list"
        :key="item.id"
        :title="item.name"
        :label="item.brand"
        @click="goDetail(item.id)"
      >
        <template #right-icon>
          <span class="price">¥{{ item.current_price }}</span>
        </template>
      </van-cell>
    </van-list>

    <van-empty v-if="list.length === 0 && !loading" description="还没有自选商品" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../utils/api'

const router = useRouter()
const list = ref([])
const loading = ref(false)
const finished = ref(false)

const loadData = async () => {
  loading.value = true
  try {
    const res = await api.listFavorites()
    if (res.data.code === 0) {
      list.value = res.data.data
      finished.value = true
    }
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const goDetail = (id) => {
  router.push({ name: '商品详情', params: { id } })
}

onMounted(() => {
  loadData()
})
</script>

<style lang="less" scoped>
.my-favorites {
  min-height: 100vh;
  background: #f7f8fa;
  
  .price {
    color: #ee0a24;
    font-weight: bold;
    font-size: 16px;
  }
}
</style>
