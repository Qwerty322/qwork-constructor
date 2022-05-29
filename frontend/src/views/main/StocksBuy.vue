<template>
  <v-container fluid>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Stocks for buying</div>
      </v-card-title>
      <v-card-text>
        <v-container
            fluid
            grid-list-lg
        >
          <v-layout row wrap>
            <v-flex xs12 v-for="stock in stockForBuy">
              <v-card>
                <v-card-title primary-title>
                  <div class="headline">Ticker:
                    <a target="_blank"
                       rel="noopener noreferrer"
                       :href="stock.url">
                      {{ stock.ticker }}
                    </a>
                  </div>
                  <v-spacer></v-spacer>
                  <span class="green--text">Price: {{ stock.price }}₽</span>
                </v-card-title>
                <v-card-text>
                  {{ stock.desc }}
                </v-card-text>
                <v-card-actions>
                  <div>
                    <v-text-field
                        label="Quantity"
                        v-model="qty"
                        required
                    ></v-text-field>
                  </div>
                  <v-btn @click="addToPortfolio(stock.id)">Add to portfolio</v-btn>
                </v-card-actions>
              </v-card>
            </v-flex>
          </v-layout>
        </v-container>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import {Component, Vue} from 'vue-property-decorator';
import {readStocksForBuy, readUserProfile} from '@/store/main/getters';
import {IPortfolio} from "@/interfaces";
import {dispatchAddToPortfolio, dispatchGetPortfolio} from "@/store/main/actions";

@Component
export default class Dashboard extends Vue {
  public qty: number = 0;

  get greetedUser() {
    const userProfile = readUserProfile(this.$store);
    if (userProfile) {
      if (userProfile.full_name) {
        return userProfile.full_name;
      } else {
        return userProfile.email;
      }
    }
  }

  get stockForBuy() {
    return readStocksForBuy(this.$store);
  }

  public async addToPortfolio(id: number) {
    const item: IPortfolio = {};
    item.qty = this.qty;
    item.stock_id = id;
    await dispatchAddToPortfolio(this.$store, item);
    await dispatchGetPortfolio(this.$store);
  }

}
</script>
