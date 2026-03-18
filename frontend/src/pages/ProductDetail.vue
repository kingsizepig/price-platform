<template>
  <div class="product-detail" v-if="product">
    <!-- 商品基本信息 -->
    <van-card :desc="product.brand" :title="product.name">
      <div v-if="product.origin_place" class="info-row">
        <span class="label">产地：</span>
        <span>{{ product.origin_place }}</span>
      </div>
      <div v-if="product.specs && Object.keys(product.specs).length > 0" class="specs">
        <div v-for="(value, key) in product.specs" :key="key" class="info-row">
          <span class="label">{{ key }}：</span>
          <span>{{ value }}</span>
        </div>
      </div>
    </van-card>

    <!-- 当前价格 -->
    <div class="price-card">
      <div class="price-label">当前价格</div>
      <div class="price-value">
        <span class="currency">¥</span>
        {{ price.current }}
      </div>
      <div class="price-source">
        <van-tag v-if="price.source === 'admin'" type="primary">官方维护</van-tag>
        <van-tag v-else type="default">用户加权平均</van-tag>
      </div>
    </div>

    <!-- 价格统计 -->
    <div v-if="price.stats" class="stats-card">
      <van-grid :column-num="3">
        <van-grid-item text="最低" :content="'¥' + price.stats.min" />
        <van-grid-item text="最高" :content="'¥' + price.stats.max" />
        <van-grid-item text="中位数" :content="'¥' + price.stats.median" />
      </van-grid>
    </div>

    <!-- 按地区对比 -->
    <div v-if="price.by_location && Object.keys(price.by_location).length > 0" class="compare-card">
      <h3>不同地区价格对比</h3>
      <div class="compare-list">
        <div v-for="(avg, loc) in price.by_location" :key="loc" class="compare-item">
          <span class="loc-name">{{ loc }}</span>
          <span class="loc-price">¥{{ avg }}</span>
        </div>
      </div>
    </div>

    <!-- 按渠道对比 -->
    <div v-if="price.by_channel && Object.keys(price.by_channel).length > 0" class="compare-card">
      <h3>不同渠道价格对比</h3>
      <div class="compare-list">
        <div v-for="(avg, channel) in price.by_channel" :key="channel" class="compare-item">
          <span class="loc-name">{{ channelName(channel) }}</span>
          <span class="loc-price">¥{{ avg }}</span>
        </div>
      </div>
    </div>

    <!-- 价格走势占位 -->
    <div class="trend-card">
      <h3>价格走势（按月）</h3>
      <div id="trend-chart" style="width: 100%; height: 200px;"></div>
    </div>

    <!-- 底部操作栏 -->
    <div class="bottom-actions">
      <van-button type="primary" size="large" block @click="addFavorite">
        {{ isFavorite ? '已加入自选' : '加入自选' }}
      </van-button>
      <van-button type="warning" size="large" block @click="goAddPrice">
        我要录入价格
      </van-button>
    </div>
  </div>

  <van-loading v-else loading />
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import * as echarts from 'echarts'
import api from '../utils/api'
import { showToast, showConfirmDialog } from 'vant'

const route = useRoute()
const router = useRouter()
const productId = route.params.id

const product = ref(null)
const price = ref({})
const isFavorite = ref(false)
let chartInstance = null

const channelMap = {
  'offline': '线下门店',
  'online': '线上电商',
  'secondhand': '二手交易',
  'auction': '拍卖',
}

const channelName = (channel) => channelMap[channel] || channel

const loadDetail = async () => {
  try {
    const res = await api.productDetail(productId)
    if (res.data.code === 0) {
      product.value = res.data.data.product
      price.value = res.data.data.price
      
      // 延迟绘制图表
      setTimeout(() => {
        initChart()
      }, 100)
    } else {
      showToast(res.data.message)
    }
  } catch (e) {
    showToast('加载失败')
  }
}

const initChart = () => {
  // TODO: 需要历史数据才能绘制走势图，后续实现
  const chartDom = document.getElementById('trend-chart')
  if (!chartDom) return
  
  chartInstance = echarts.init(chartDom)
  const option = {
    xAxis: {
      type: 'category',
      data: ['1月', '2月', '3月', '4月', '5月', '6月'],
    },
    yAxis: {
      type: 'value',
    },
    series: [{
      data: [price.value.current || 0],
      type: 'line',
      smooth: true,
    }],
    tooltip: {
      trigger: 'axis',
    },
  }
  chartInstance.setOption(option)
}

const addFavorite = async () => {
  try {
    if (isFavorite.value) {
      await api.removeFavorite(productId)
      isFavorite.value = false
      showToast('已移除自选')
    } else {
      await api.addFavorite(productId)
      isFavorite.value = true
      showToast('已加入自选')
    }
  } catch (e) {
    showToast('操作失败')
  }
}

const goAddPrice = () => {
  router.push({ name: '录入价格', params: { productId } })
}

onMounted(() => {
  loadDetail()
})

onUnmounted(() => {
  if (chartInstance) {
    chartInstance.dispose()
  }
})
</script>

<style lang="less" scoped>
.product-detail {
  padding-bottom: 100px;
}

.info-row {
  display: flex;
  margin: 6px 0;
  font-size: 14px;
  
  .label {
    color: #666;
  }
  
  span:last-child {
    color: #333;
    flex: 1;
  }
}

.specs {
  margin-top: 10px;
}

.price-card {
  background: white;
  margin: 10px;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  
  .price-label {
    font-size: 14px;
    color: #666;
  }
  
  .price-value {
    font-size: 36px;
    font-weight: bold;
    color: #ee0a24;
    margin: 10px 0;
    
    .currency {
      font-size: 20px;
    }
  }
  
  .price-source {
    margin-top: 10px;
  }
}

.stats-card {
  background: white;
  margin: 10px;
  padding: 15px;
  border-radius: 8px;
}

.compare-card {
  background: white;
  margin: 10px;
  padding: 15px;
  border-radius: 8px;
  
  h3 {
    font-size: 15px;
    color: #333;
    margin-bottom: 10px;
  }
  
  .compare-list {
    .compare-item {
      display: flex;
      justify-content: space-between;
      padding: 8px 0;
      border-bottom: 1px solid #f0f0f0;
      
      &:last-child {
        border-bottom: none;
      }
      
      .loc-name {
        color: #333;
      }
      
      .loc-price {
        font-weight: bold;
        color: #ee0a24;
      }
    }
  }
}

.trend-card {
  background: white;
  margin: 10px;
  padding: 15px;
  border-radius: 8px;
  
  h3 {
    font-size: 15px;
    color: #333;
    margin-bottom: 10px;
  }
}

.bottom-actions {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 10px;
  background: white;
  box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
  
  .van-button {
    margin: 5px 0;
  }
}
</style>
