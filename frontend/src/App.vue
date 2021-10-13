<template>
  <div>
    <div id="title-bar">
      <div id="title">TaskVis: Task-oriented Visualization Recommendation</div>
    </div>

    <div id="main-part">
      <div id="left-part">
        <!--   最左侧的窗口,用于选择Data和Setting   -->
        <el-card id="data-card"
                 class="card">
          <div slot="header"
               class="clearfix">
            <span>Data</span>
          </div>
          <el-select v-model="dataset_value"
                     placeholder="Choosing a Dataset"
                     @change="choose_dataset">
            <el-option v-for="item in dataset_options"
                       :key="item.value"
                       :label="item.label"
                       :value="item.value">
            </el-option>
          </el-select>
          <el-divider></el-divider>
          <div id="data-box">
            <div class="data-item"
                 v-for="item in data_list"
                 v-bind:key="item.field">
              <div class="data-item-icon"></div>
              <div class="data-item-field">{{item.field}}</div>
            </div>
          </div>
        </el-card>

        <el-card id="setting-card"
                 class="card">
          <div slot="header"
               class="clearfix">
            <span>Setting</span>
          </div>
          <div id="max-number-of-charts">
            <div class="setting-title">Max Number of Charts</div>
            <el-input-number id="max-number-of-charts-input"
                             v-model="max_number_of_charts"
                             :min="1"
                             size="medium"></el-input-number>
          </div>
          <el-divider></el-divider>
          <div id="recommendation-mode">
            <div class="setting-title">Recommendation Mode</div>
            <el-radio v-model="recommendation_mode_radio"
                      label="1">Individual Recommendation</el-radio>
            <el-radio v-model="recommendation_mode_radio"
                      label="2">Combination Recommendation</el-radio>
          </div>
          <el-divider></el-divider>
          <div id="ranking-scheme">
            <div class="setting-title">Ranking Scheme</div>
            <el-radio v-model="ranking_scheme_radio"
                      label="1">Complexity-based ranking</el-radio>
            <el-radio v-model="ranking_scheme_radio"
                      label="2">Reverse-complexity-based ranking</el-radio>
            <el-radio v-model="ranking_scheme_radio"
                      label="3">Interested-data-columns-based ranking</el-radio>
            <el-radio v-model="ranking_scheme_radio"
                      label="4">Tasks-coverage-based ranking</el-radio>
          </div>
        </el-card>
        <el-button id="recommendation-button"
                   type="primary"
                   @click="recommendation">Recommendation</el-button>
      </div>

      <div id="mid-part">
        <!--    中间的窗口，用于选择Task List    -->
        <el-card id="task-list-card"
                 class="card">
          <div slot="header"
               class="clearfix">
            <span>Task List</span>
          </div>
        </el-card>
      </div>
      <div id="right-part"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'App',
  data () {
    return {
      dataset_options: [{
        value: 'cars',
        label: 'Cars'
      }, {
        value: 'movies',
        label: 'Movie'
      }, {
        value: 'weather',
        label: 'Weather'
      }],
      data_type: {
        'temporal': 'T',
        'quantitative': 'Q',
        'nominal': 'N',
        'ordinal': 'O'
      },
      dataset_value: '',
      max_number_of_charts: 10,
      recommendation_mode_radio: '1',
      ranking_scheme_radio: '1',
      data_list: []
    }
  },
  methods: {
    choose_dataset (dataset) {
      this.dataset_value = dataset
      // TODO 向服务器发送请求获取数据，获取推荐参数
      console.log('select dataset ' + dataset)
      this.$axios.get('api/columns?dataset=' + dataset)
        .then(Response => {
          this.data_list = Response.data
          console.log(this.data_list)
        })
    },

    recommendation () {
      // TODO 将选中的数据发送到服务器，获取推荐图表
    }
  }
}
</script>

<style>
#title {
  font-size: 25px;
  color: white;
  padding: 16px;
}

#title-bar {
  background: dodgerblue;
}

#main-part {
  display: flex;
  flex-direction: row;
  height: 100%;
}

#left-part {
  width: 350px;
  display: flex;
  flex-direction: column;
  margin-right: 5px;
}

#mid-part {
  width: 350px;
  margin-right: 5px;
  min-height: 90%;
}

#right-part {
  width: auto;
}

#max-number-of-charts {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.card {
  margin-bottom: 10px;
}

.setting-title {
  margin-bottom: 10px;
}

#task-list-card {
  min-height: 90%;
}

.data-item {
  display: flex;
  flex-direction: row;
  align-items: center;
}

.data-item-field {
  margin-left: 5px;
}
</style>
