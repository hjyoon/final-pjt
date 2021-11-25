<template>
  <v-col cols="12">
    <v-card>
      <v-list-item class="grow" dense>
        <v-list-item-avatar color="grey darken-3" size="40">
          <v-img
            src="https://avataaars.io/?avatarStyle=Transparent&topType=ShortHairShortCurly&accessoriesType=Prescription02&hairColor=Black&facialHairType=Blank&clotheType=Hoodie&clotheColor=White&eyeType=Default&eyebrowType=DefaultNatural&mouthType=Default&skinColor=Light"
          ></v-img>
        </v-list-item-avatar>
        <v-list-item-content>
          <v-list-item-title>{{ comment.user.username }}</v-list-item-title>
          <v-list-item-subtitle>{{
            timeForToday(comment.created_at)
          }}</v-list-item-subtitle>
        </v-list-item-content>
        <v-list-item-content>
          <v-card-text v-if="edit == false">{{ comment.content }}</v-card-text>
          <v-text-field
            v-if="edit"
            v-model="comment.content"
            placeholder="댓글을 입력하세요"
            outlined
            dense
            hide-details="false"
            rounded
            @keydown.enter="updateComment(comment)"
          ></v-text-field>
        </v-list-item-content>
        <v-card-actions>
          <v-btn
            icon
            @click="editMode(true)"
            v-if="comment.user.id == tokenInfo.user_id"
          >
            <v-icon>mdi-note-edit</v-icon>
          </v-btn>
          <v-btn
            icon
            @click="deleteComment(comment)"
            v-if="comment.user.id == tokenInfo.user_id"
          >
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </v-card-actions>
      </v-list-item>
    </v-card>
  </v-col>
</template>

<script>
import { mapState, mapActions } from "vuex";

export default {
  name: "CommentListCard",
  props: {
    comment: Object,
  },
  data: () => ({
    edit: false,
  }),
  methods: {
    editMode: function (b) {
      this.edit = b;
    },
    updateComment: function (comment) {
      (async () => {
        const token = localStorage.getItem("jwt");
        const URL = `https://www.movie-vol.ga/community/${comment.article}/comments/${comment.id}/`;
        const response = await fetch(URL, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: `JWT ${token}`,
          },
          body: JSON.stringify({ content: comment.content }),
        });
        if (response.ok) {
          //const data = await response.json();
          //console.log(data);
          this.$router.go();
          //this.openCommentDialog();
        }
      })();
      this.editMode(false);
    },
    deleteComment: function (comment) {
      (async () => {
        const token = localStorage.getItem("jwt");
        const URL = `https://www.movie-vol.ga/community/${comment.article}/comments/${comment.id}/`;
        const response = await fetch(URL, {
          method: "DELETE",
          headers: {
            Authorization: `JWT ${token}`,
          },
        });
        if (response.ok) {
          //const data = await response.json();
          //console.log(data);
          this.$router.go();
          //this.openCommentDialog();
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
    ...mapActions([]),
  },
  computed: {
    ...mapState(["tokenInfo"]),
  },
};
</script>

<style></style>
