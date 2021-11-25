import Vue from "vue";
import Vuex from "vuex";
import router from "../router";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    isLogin: false,
    tokenInfo: null,
    app_title: "",
    selected_menu: 0,
    drawer: false,
    dialog: false,
    dialog_movie_data: { videos: [{}] },
    similar_movies: {},
    write_dialog: false,
    update_mode: false,
    tmp_article: { id: null, movie_title: null, content: null, rating: null },
    comment_dialog: false,
    comment_list: [],
  },
  mutations: {
    DO_REGISTRATION: function () {},
    DO_LOGIN: function (state) {
      state.isLogin = true;
      const token = localStorage.getItem("jwt");
      const atob = (str) => Buffer.from(str, "base64").toString("binary"); // atob 가 deprecated 이므로 대신 사용
      state.tokenInfo = JSON.parse(atob(token.split(".")[1]));
    },
    DO_LOGOUT: function (state) {
      localStorage.removeItem("jwt");
      state.isLogin = false;
    },
    SET_APP_TITLE: function (state, title) {
      state.app_title = title;
    },
    SET_SELECTED_MENU: function (state, id) {
      state.selected_menu = id;
    },
    SET_DRAWER: function (state) {
      state.drawer = true;
    },
    CHANGE_ROUTE: function (state, route) {
      router.push(route);
    },
    OPEN_DIALOG: function (state) {
      state.dialog = true;
    },
    CLOSE_DIALOG: function (state) {
      state.dialog = false;
      state.dialog_movie_data = { videos: [{}] };
    },
    LOAD_DIALOG: function (state, data) {
      state.dialog_movie_data = data;
    },
    LOAD_DIALOG_SIMILAR: function (state, data) {
      state.similar_movies = data;
    },
    OPEN_WRITE_DIALOG: function (state) {
      state.write_dialog = true;
    },
    SET_UPDATE_MODE: function (state, b) {
      state.update_mode = b;
    },
    SET_TMP_ARTICLE: function (state, data) {
      state.tmp_article = data;
    },
    SET_COMMENT_LIST: function (state, data) {
      state.comment_list = data;
    },
    CLOSE_WRITE_DIALOG: function (state) {
      state.write_dialog = false;
      state.update_mode = false;
      state.tmp_article = {
        id: null,
        movie_title: null,
        content: null,
        rating: null,
      };
    },
    OPEN_COMMENT_DIALOG: function (state) {
      state.comment_dialog = true;
    },
    CLOSE_COMMENT_DIALOG: function (state) {
      state.comment_dialog = false;
    },
  },
  actions: {
    doRegistration: function (context, credentials) {
      if (credentials.username.length < 5) {
        alert("username을 최소 5자 이상으로 입력해주세요.");
        return;
      }
      if (credentials.password.length < 5) {
        alert("password을 최소 5자 이상으로 입력해주세요.");
        return;
      }
      if (credentials.password != credentials.confirm_password) {
        alert("비밀번호가 일치하지 않습니다.");
        return;
      }

      (async () => {
        const URL = "https://www.movie-vol.ga/accounts/register/";
        const response = await fetch(URL, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            username: credentials.username,
            password: credentials.password,
          }),
        });
        // HTTP 상태 코드가 200과 299 사이일 경우 true
        if (response.ok) {
          // const data = await response.json();
          context.commit("DO_REGISTRATION");
          context.commit("CHANGE_ROUTE", { name: "Login" });
        } else {
          alert("회원가입에 실패하였습니다.");
        }
      })();
    },
    doLogin: function (context, credentials) {
      (async () => {
        const URL = "https://www.movie-vol.ga/accounts/login/";
        const response = await fetch(URL, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(credentials),
        });

        // HTTP 상태 코드가 200과 299 사이일 경우 true
        if (response.ok) {
          const data = await response.json();
          localStorage.setItem("jwt", data.token);
          context.commit("DO_LOGIN");
          context.commit("CHANGE_ROUTE", { name: "Home" });
        } else {
          alert("로그인에 실패하였습니다.");
        }
      })();
    },
    doAutoLogin: function (context) {
      const token = localStorage.getItem("jwt");
      if (token) {
        context.commit("DO_LOGIN");
      }
    },
    doLogout: function (context) {
      context.commit("DO_LOGOUT");
      context.commit("CHANGE_ROUTE", { name: "Home" });
    },
    setAppTitle: function (context, title) {
      context.commit("SET_APP_TITLE", title);
    },
    setSelectedMenu: function (context, id) {
      context.commit("SET_SELECTED_MENU", id);
    },
    setDrawer: function (context) {
      context.commit("SET_DRAWER");
    },
    changeRoute: function (context, route) {
      context.commit("CHANGE_ROUTE", route);
    },
    openDialog: function (context, movie_id) {
      (async () => {
        const token = localStorage.getItem("jwt");
        const URL = `https://www.movie-vol.ga/movies/${movie_id}`;
        const response = await fetch(URL, {
          method: "GET",
          headers: {
            Authorization: context.state.isLogin ? `JWT ${token}` : "",
          },
        });
        if (response.ok) {
          const data = await response.json();
          if (data.rating_count > 0) {
            data.rating_average = data.rating_average.toFixed(1);
          }
          context.commit("LOAD_DIALOG", data);
        }
      })();
      (async () => {
        const URL = `https://www.movie-vol.ga/movies/recommend/?source=${movie_id}&count=4`;
        const response = await fetch(URL);
        if (response.ok) {
          const data = await response.json();
          //console.log(data);
          context.commit("LOAD_DIALOG_SIMILAR", data);
        }
      })();
      context.commit("OPEN_DIALOG");
    },
    closeDialog: function (context) {
      context.commit("CLOSE_DIALOG");
    },
    openWriteDialog: function (context) {
      context.commit("OPEN_WRITE_DIALOG");
    },
    setUpdateMode: function (context, b) {
      context.commit("SET_UPDATE_MODE", b);
    },
    setTmpArticle: function (context, data) {
      context.commit("SET_TMP_ARTICLE", data);
    },
    closeWriteDialog: function (context) {
      context.commit("CLOSE_WRITE_DIALOG");
    },
    openCommentDialog: function (context) {
      context.commit("OPEN_COMMENT_DIALOG");
    },
    closeCommentDialog: function (context) {
      context.commit("CLOSE_COMMENT_DIALOG");
    },
    setCommentList: function (context, data) {
      context.commit("SET_COMMENT_LIST", data);
    },
  },
});
