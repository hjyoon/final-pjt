<template>
  <v-col cols="12">
    <v-card>
      <v-list-item class="grow">
        <v-list-item-avatar color="grey darken-3">
          <v-img
            class="elevation-6"
            alt=""
            src="https://avataaars.io/?avatarStyle=Transparent&topType=ShortHairShortCurly&accessoriesType=Prescription02&hairColor=Black&facialHairType=Blank&clotheType=Hoodie&clotheColor=White&eyeType=Default&eyebrowType=DefaultNatural&mouthType=Default&skinColor=Light"
          ></v-img>
        </v-list-item-avatar>
        <v-list-item-content>
          <v-list-item-title>{{ article.user.username }}</v-list-item-title>
          <v-list-item-subtitle>{{ article.movie_title }}</v-list-item-subtitle>
          <v-rating
            :value="article.rating"
            color="amber"
            size="12"
            dense
            readonly
          ></v-rating>
        </v-list-item-content>
        <v-list-item-content>
          <v-list-item-subtitle>{{
            timeForToday(article.created_at)
          }}</v-list-item-subtitle>
        </v-list-item-content>
        <v-card-actions v-if="article.user.id == tokenInfo.user_id">
          <v-btn icon @click="updateArticle(article)">
            <v-icon>mdi-note-edit</v-icon>
          </v-btn>
          <v-btn icon @click="deleteArticle(article.id)">
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </v-card-actions>
      </v-list-item>
      <v-divider class="mx-4"></v-divider>
      <v-card-text>{{ article.content }}</v-card-text>
      <v-divider class="mx-4"></v-divider>
      <v-card-text>
        <a @click="updateCommentList(article.id)"
          >댓글 {{ article.comment_count }}개 모두 보기</a
        >
      </v-card-text>
      <v-list-item class="grow">
        <v-list-item-avatar>
          <img src="https://cdn.vuetifyjs.com/images/john.jpg" alt="John" />
        </v-list-item-avatar>
        <v-list-item-content>
          <v-text-field
            v-model="comment_value"
            placeholder="댓글을 입력하세요"
            outlined
            dense
            hide-details="false"
            rounded
            @keydown.enter="createComment(article.id)"
          >
          </v-text-field>
        </v-list-item-content>
      </v-list-item>
    </v-card>
  </v-col>
</template>

<script>
import { mapState, mapActions } from "vuex";

export default {
  name: "ArticleListCard",
  props: {
    article: Object,
  },
  data: () => ({ comment_value: null }),
  methods: {
    createComment: function (id) {
      (async () => {
        const token = localStorage.getItem("jwt");
        const URL = `https://www.movie-vol.ga/community/${id}/comments/`;
        const response = await fetch(URL, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `JWT ${token}`,
          },
          body: JSON.stringify({
            content: this.comment_value,
          }),
        });
        if (response.ok) {
          this.comment_value = null;
          const data = await response.json();
          console.log(data);
          this.$router.go();
          //this.openCommentDialog();
        }
      })();
    },
    updateCommentList: function (id) {
      (async () => {
        const token = localStorage.getItem("jwt");
        const URL = `https://www.movie-vol.ga/community/${id}/comments/`;
        const response = await fetch(URL, {
          method: "GET",
          headers: {
            Authorization: `JWT ${token}`,
          },
        });

        if (response.ok) {
          //this.$router.go();
          const data = await response.json();
          console.log(data);
          this.setCommentList(data);
          this.openCommentDialog();
          // context.commit("LOAD_DIALOG", data);
        }
      })();
    },
    updateArticle: function (article) {
      this.setUpdateMode(true);
      this.setTmpArticle(article);
      this.openWriteDialog();
    },
    deleteArticle: function (id) {
      (async () => {
        const token = localStorage.getItem("jwt");
        const URL = `https://www.movie-vol.ga/community/${id}`;
        const response = await fetch(URL, {
          method: "DELETE",
          headers: {
            Authorization: `JWT ${token}`,
          },
        });
        if (response.ok) {
          this.$router.go();
          //const data = await response.json();
          //console.log(data);
          // context.commit("LOAD_DIALOG", data);
        }
      })();
    },
    timeForToday: function (value) {
      const today = new Date();
      const timeValue = new Date(value);

      const betweenTime = Math.floor(
        (today.getTime() - timeValue.getTime()) / 1000 / 60
      );
      if (betweenTime < 1) return "방금 전";
      if (betweenTime < 60) {
        return `${betweenTime}분 전`;
      }

      const betweenTimeHour = Math.floor(betweenTime / 60);
      if (betweenTimeHour < 24) {
        return `${betweenTimeHour}시간 전`;
      }

      const betweenTimeDay = Math.floor(betweenTime / 60 / 24);
      if (betweenTimeDay < 365) {
        return `${betweenTimeDay}일 전`;
      }

      return `${Math.floor(betweenTimeDay / 365)}년 전`;
    },
    ...mapActions([
      "openWriteDialog",
      "setUpdateMode",
      "setTmpArticle",
      "setCommentList",
      "openCommentDialog",
    ]),
  },
  computed: {
    ...mapState(["tokenInfo"]),
  },
};
</script>

<style></style>
