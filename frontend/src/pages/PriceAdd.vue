<template>
  <div class="price-add">
    <van-form @submit="onSubmit">
      <van-field
        v-model="form.price"
        name="price"
        label="价格"
        type="number"
        placeholder="请输入价格（元）"
        :rules="[{ required: true, message: '请输入价格' }]"
      />
      
      <van-collapse v-model="activeCollapse">
        <van-collapse-item name="1" title="高级选项（可选）">
          <van-field
            v-model="form.deal_date"
            name="deal_date"
            label="成交日期"
            placeholder="默认今天"
            readonly
            @click="showDatePicker = true"
          />
          <van-field
            v-model="form.location"
            name="location"
            label="所在地"
            placeholder="省市"
          />
          <van-picker
            v-model="form.channel"
            :columns="channelOptions"
            title="销售渠道"
          />
          <van-picker
            v-model="form.quality"
            :columns="qualityOptions"
            title="商品品相"
          />
        </van-collapse-item>
      </van-collapse>

      <div class="tip">
        默认参数已经填好了，直接提交就行 😊
      </div>

      <van-button block type="primary" native-type="submit">
        提交
      </van-button>
    </van-form>

    <van-date-picker
      v-model:show="showDatePicker"
      v-model="form.deal_date"
      @confirm="showDatePicker = false"
      @cancel="showDatePicker = false"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../utils/api'
import { showToast } from 'vant'

const route = useRoute()
const router = useRouter()
const productId = route.params.productId

const today = new Date().toISOString().split('T')[0]

const form = ref({
  price: '',
  deal_date: today,
  channel: 'offline',
  location: '',
  quality: 'new',
})

const activeCollapse = ref([])
const showDatePicker = ref(false)

const channelOptions = [
  { text: '线下门店', value: 'offline' },
  { text: '线上电商', value: 'online' },
  { text: '二手交易', value: 'secondhand' },
  { text: '拍卖', value: 'auction' },
]

const qualityOptions = [
  { text: '全新', value: 'new' },
  { text: '九成新', value: '90new' },
  { text: '七成新', value: '70new' },
  { text: '二手', value: 'used' },
  { text: '临期', value: 'expiring' },
]

const onSubmit = async () => {
  if (!form.value.price) {
    showToast('请输入价格')
    return
  }
  
  try {
    const data = {
      product_id: parseInt(productId),
      price: parseFloat(form.value.price),
      deal_date: form.value.deal_date,
      channel: form.value.channel,
      location: form.value.location || undefined,
      quality: form.value.quality,
    }
    
    const res = await api.createPrice(data)
    if (res.data.code === 0) {
      showToast('录入成功，获得积分 +5')
      router.back()
    } else {
      showToast(res.data.message)
    }
  } catch (e) {
    showToast('提交失败')
    console.error(e)
  }
}
</script>

<style lang="less" scoped>
.price-add {
  padding: 10px;
  
  .tip {
    text-align: center;
    color: #999;
    font-size: 12px;
    margin: 10px 0;
  }
}
</style>
