<template>
  <div>
    <loader v-if="isLoading || (student == undefined && employee == undefined)">
    </loader>
    <div v-else>
      <h1>Личный кабинет</h1>
      <form>
        <div class="form-row">
          <div class="form-group col-md-6">
            <label class="form-name">Фамилия: </label><br />
            <p v-if="isStudent && student != undefined">
              {{ student.user.lastName }}
            </p>
            <p v-if="!isStudent && employee != undefined">
              {{ employee.user.lastName }}
            </p>
          </div>
        </div>

        <div class="form-row">
          <div class="form-group col-md-6">
            <label class="form-name">Имя: </label><br />
            <p v-if="isStudent && student != undefined">
              {{ student.user.firstName }}
            </p>
            <p v-if="!isStudent && employee != undefined">
              {{ employee.user.firstName }}
            </p>
          </div>
        </div>

        <div class="form-row" v-if="isStudent && student != undefined">
          <div class="form-group col-md-6">
            <label class="form-name">Отчество:</label><br />
            <p v-if="!edit">{{ isNullOrEmpty(student.patronymic) }}</p>
            <input
              v-else
              id="patronymic"
              type="text"
              class="form-control"
              v-model.trim="formStudent.patronymic"
            />
          </div>
        </div>
        <div class="form-row" v-if="isStudent && student != undefined">
          <div class="form-group col-md-6">
            <label class="form-name">Дата рождения:</label><br />
            <p v-if="!edit">
              {{ isNullOrEmpty(formatDate(student.birthdate)) }}
            </p>
            <input
              v-else
              class="form-control"
              id="birthdate"
              type="date"
              v-model="formStudent.birthdate"
              :max="new Date().toISOString().substr(0, 10)"
            />
          </div>
        </div>
        <div class="form-row" v-if="!isStudent && employee != undefined">
          <div class="form-group col-md-6">
            <label class="form-name">Организация: </label><br />
            <p>{{ employee.organization.fullname }}</p>
          </div>
        </div>
        <div class="form-row" v-if="!isStudent && employee != undefined">
          <div class="form-group col-md-6">
            <label class="form-name">Должность:</label><br />
            <p v-if="!edit">{{ isNullOrEmpty(employee.position) }}</p>
            <input
              v-else
              id="position"
              class="form-control"
              type="text"
              v-model.trim="formEmployee.position"
            />
          </div>
        </div>
        <div class="form-row">
          <div class="form-group col-md-6">
            <label class="form-name">E-mail </label><br />
            <p v-if="!isStudent && employee != undefined">
              {{ employee.user.email }}
            </p>
            <p v-if="isStudent && student != undefined">
              {{ student.user.email }}
            </p>
          </div>
        </div>
      </form>
      <div v-if="edit" @click="onEdit">
        <button class="text-gradient to-block">
          Сохранить
          <span class="text">Сохранить</span>
        </button>
      </div>
      <div v-if="!edit" @click="onEdit">
        <button class="text-gradient to-block">
          Изменить
          <span class="text">Изменить</span>
        </button>
      </div>
      <br />
      <p>
        <router-link
          tag="a"
          class="text-decoration-none"
          :to="{ name: 'DeleteAccount' }"
          >Удалить аккаунт</router-link
        >
      </p>
    </div>
  </div>
</template>

<script>
import Multiselect from "vue-multiselect";
import { EMPLOYEE, STUDENT } from "@/graphql/queries/queries";
import jwt from "jsonwebtoken";
import { UPDATE_EMPLOYEE, UPDATE_STUDENT } from "@/graphql/mutations/mutations";
import Loader from "@/components/parts/Loader.vue";

export default {
  name: "Profile",
  components: {
    Multiselect,
    Loader,
  },
  apollo: {
    student: {
      query: STUDENT,
      variables() {
        return {
          userId: this.userId,
        };
      },
    },
    employee: {
      query: EMPLOYEE,
      variables() {
        return {
          userId: this.userId,
        };
      },
    },
  },
  data() {
    return {
      formStudent: {
        patronymic: undefined,
        birthdate: undefined,
      },
      formEmployee: {
        position: undefined,
      },
      edit: false,
      submittedForm: false,
    };
  },

  computed: {
    organizationId() {
      return jwt.decode(localStorage.getItem("token")).organization_id;
    },
    userId() {
      return jwt.decode(localStorage.getItem("token")).user_id;
    },
    isLoading() {
      return this.$store.state.isLoading;
    },
    isStudent() {
      return this.$store.state.isStudent;
    },
  },
  methods: {
    isNullOrEmpty(str) {
      if (str == null || str == undefined || str == "") return "-";
      else return str;
    },
    formatDate(date) {
      if (!date) return null;
      const [year, month, day] = date.split("-");
      return `${day}.${month}.${year}`;
    },

    onEdit() {
      if (this.isStudent) {
        if (!this.edit) {
          this.edit = true;
          this.formStudent.patronymic = this.student.patronymic;
          this.formStudent.birthdate = this.student.birthdate;
        } else {
          this.submittedForm = true;
          this.$store.commit("START_LOADING");
          this.$apollo
            .mutate({
              mutation: UPDATE_STUDENT,
              variables: {
                userId: this.userId,
                patronymic: this.formStudent.patronymic,
                birthdate: this.formStudent.birthdate,
              },
            })
            .then(() => {
              this.$apollo.queries.student.refresh();
              this.$apollo.queries.student.refetch();
            })
            .catch((error) => {
              console.error(error);
            });
          this.edit = false;
          this.$store.commit("STOP_LOADING");
        }
      } else {
        if (!this.edit) {
          this.edit = true;
          this.formEmployee.position = this.employee.position;
        } else {
          this.$store.commit("START_LOADING");
          this.$apollo
            .mutate({
              mutation: UPDATE_EMPLOYEE,
              variables: {
                employeeId: this.employee.id,
                position: this.formEmployee.position,
              },
            })
            .then(() => {
              this.$apollo.queries.employee.refresh();
              this.$apollo.queries.employee.refetch();
            })
            .catch((error) => {
              console.error(error);
            });
          this.edit = false;
          this.$store.commit("STOP_LOADING");
        }
      }
    },
  },
};
</script>
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<style lang="scss"></style>
