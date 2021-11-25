<template>
  <v-container>
    <p class="text-justify" v-if="isLogin"></p>
    <p class="text-justify" v-else>로그인을 먼저 해주세요.</p>
  </v-container>
</template>

<script>
import { mapState, mapActions } from "vuex";

export default {
  name: "Favorites",
  components: {},
  methods: {
    ...mapActions(["setAppTitle", "setSelectedMenu"]),
  },
  computed: {
    ...mapState(["isLogin"]),
  },
  created: function () {
    this.setAppTitle("Favorites");
    this.setSelectedMenu(3);
  },
};
</script>
