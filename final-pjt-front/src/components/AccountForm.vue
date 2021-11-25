<template>
  <div class="account-form">
    <p class="text-justify" v-if="isLogin">
      {{ tokenInfo.username }} 님 환영합니다.
    </p>
    <p class="text-justify" v-else>로그인을 먼저 해주세요.</p>
  </div>
</template>

<script>
import { mapState } from "vuex";

export default {
  name: "AccountForm",
  data: function () {
    return {};
  },
  computed: {
    ...mapState(["isLogin", "tokenInfo"]),
  },
};
</script>

<style></style>
