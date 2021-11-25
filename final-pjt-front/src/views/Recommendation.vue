<template>
  <v-container>
    <p class="text-justify" v-if="!isLogin">로그인을 먼저 해주세요.</p>
    <RecommendMovieList v-if="isLogin"></RecommendMovieList>
  </v-container>
</template>

<script>
import RecommendMovieList from "@/components/RecommendMovieList.vue";
import { mapState, mapActions } from "vuex";

export default {
  name: "Recommendation",
  components: { RecommendMovieList },
  methods: {
    ...mapActions(["setAppTitle", "setSelectedMenu"]),
  },
  computed: {
    ...mapState(["isLogin"]),
  },
  created: function () {
    this.setAppTitle("Recommendation");
    this.setSelectedMenu(4);
  },
};
</script>
