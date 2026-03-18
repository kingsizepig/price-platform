<template>
  <div class="category-list">
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
      />
    </van-list>

    <van-empty v-if="list.length === 0 && !loading" description="该分类下暂无商品" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../utils/api'

const route = useRoute()
const router = useRouter()
const categoryId = route.params.id
const list = ref([])
const loading = ref(false)
const finished = ref(false)
const page = ref(1)

const loadData = async () => {
  loading.value = true
  try {
    const res = await api.listByCategory(categoryId, page.value)
    if (res.data.code === 0) {
      if (page.value === 1) {
        list.value = res.data.data.list
      } else {
        list.value.push(...res.data.data.list)
      }
      finished.value = res.data.data.list.length < 20
      page.value++
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
.category-list {
  min-height: 100vh;
  background: #f7f8fa;
}
</style>
