<template>
  <v-container fluid>
    <v-card>
      <v-card-title>
        <div class="headline primary--text">Stocks</div>
        <v-spacer></v-spacer>
        <v-text-field
            v-model="search"
            append-icon="mdi-magnify"
            label="Search"
            single-line
            hide-details
        ></v-text-field>
      </v-card-title>

      <v-data-table
          :headers="headers"
          :items="stock"
          :search="search"
          class="elevation-1"
      >
        <template v-slot:items="props">

          <td>{{ props.item.name }}</td>
          <td>{{ props.item.symbol }}</td>
          <td>{{ props.item.currency }}</td>
          <td>{{ props.item.last }}</td>
          <td>{{ props.item.high }}</td>
          <td>{{ props.item.low }}</td>
          <td>{{ props.item.change }}</td>
          <td>{{ props.item.change_percentage }}</td>
          <td>{{ props.item.turnover }}</td>

        </template>
      </v-data-table>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import {Component, Vue} from 'vue-property-decorator';
import {readStocks} from '@/store/main/getters';

@Component
export default class Stocks extends Vue {
  public qty: number = 0;
  public headers = [
    {
      text: 'Stock name',
      align: 'start',
      sortable: false,
      value: 'name',
    },
    {text: 'Ticker', value: 'symbol'},
    {text: 'Currency', value: 'currency'},
    {text: 'Last price', value: 'last'},
    {text: 'High price', value: 'high'},
    {text: 'Low price', value: 'low'},
    {text: 'Change', value: 'change'},
    {text: 'Change (%)', value: 'change_percentage'},
    {text: 'Turnover', value: 'turnover'},
  ];
  public search: string = '';


  public get stock() {
    return readStocks(this.$store);
  }

  // public async addToPortfolio(id: number) {
  //   const item: IPortfolio = {};
  //   item.qty = this.qty;
  //   item.stock_id = id;
  //   await dispatchAddToPortfolio(this.$store, item);
  //   await dispatchGetPortfolio(this.$store);
  // }

}
</script>
