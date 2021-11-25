<template>
  <div>
    <v-row>
      <ArticleListCard
        v-for="article in articles"
        :key="article.id"
        :article="article"
      ></ArticleListCard>
    </v-row>
    <InfiniteLoading @infinite="infiniteHandler" spinner="waveDots">
    </InfiniteLoading>
  </div>
</template>

<script>
import { mapState } from "vuex";
import InfiniteLoading from "vue-infinite-loading";
import ArticleListCard from "@/components/ArticleListCard.vue";

export default {
  name: "ArticleList",
  components: { InfiniteLoading, ArticleListCard },
  data: () => ({
    page: 1,
    articles: [],
  }),
  methods: {
    infiniteHandler: function ($state) {
      const EACH_LEN = 20;
      (async () => {
        //const URL = `https://www.movie-vol.ga/community/?page=${page}`;
        const token = localStorage.getItem("jwt");
        const URL = `https://www.movie-vol.ga/community/`;
        const response = await fetch(URL, {
          method: "GET",
          headers: {
            Authorization: `JWT ${token}`,
          },
        });
        if (response.ok) {
          const data = await response.json();
          console.log(data);
          this.articles.push(...data);
          this.page += 1;
          $state.loaded();
          if (data.length / EACH_LEN < 1) {
            $state.complete();
          }
        } else {
          alert("fail");
        }
      })();
    },
  },
  computed: {
    ...mapState([]),
  },
};
</script>

<style></style>
