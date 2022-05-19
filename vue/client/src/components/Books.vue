<template>
  <div class="container">
    <div class="col-sm-10">
      <nav class="navbar navbar-durham">
        <a class="navbar-brand logo-durham mx-auto">
          <h1>Email validator</h1>
        </a>
      </nav>
      <h4>Developed by Sadullaev Muzaffar HSE FCS AMI</h4>
      <hr />
      <br />
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
        <b-form-group
          id="form-title-group"
          label="Email validation:"
          label-for="form-title-input"
        >
          <b-form-input
            id="form-title-input"
            type="text"
            v-model="addBookForm.email"
            required
            placeholder="Enter email"
          >
          </b-form-input>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary"
            :style="'margin-bottom: 20px'">Validate email</b-button>
        </b-button-group>
        <h4 v-bind:style="{ color: result_color}">{{ message }}</h4>
         <tr v-for="parameter in response_data" :key="parameter">
              <h4>{{ parameter }}</h4>
          </tr>
      </b-form>
    </div>
  </div>
</template>

<style>
.logo-durham {
  font-family: "arcade-classic", Arial, sans-serif;
  background-color: white;
  color: black;
  word-spacing: 10px;
  text-align: center;
}

.logo-durham:hover {
  -webkit-animation: rainbow-font 3s ease-in-out infinite;
  -z-animation: rainbow-font 3s ease-in-out infinite;
  -o-animation: rainbow-font 3s ease-in-out infinite;
  animation: rainbow-font 3s linear infinite;
}

@-webkit-keyframes rainbow-font {
  0%,
  100% {
    color: #ff2400;
  }
  11% {
    color: #e81d1d;
  }
  22% {
    color: #e8b71d;
  }
  33% {
    color: #e3e81d;
  }
  44% {
    color: #1de840;
  }
  55% {
    color: #1ddde8;
  }
  66% {
    color: #2b1de8;
  }
  77% {
    color: #dd00f3;
  }
  88% {
    color: #dd00f3;
  }
}
</style>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      response_data: {
        is_email_valid: '',
        is_email_free: '',
        is_email_one_time: '',
        deliverability: '',
        mailgun: '',
      },
      addBookForm: {
      },
      message: '',
      result_color: 'red',
    };
  },
  methods: {
    getBooks() {
      const path = 'http://localhost:5000/books';
      axios.get(path)
        .then((res) => {
          this.response_data = res.data.books;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addBook(payload) {
      const path = 'http://localhost:5000/validate';
      axios.post(path, payload)
        .then((res) => {
          this.message = res.data.message;
          this.response_data = res.data.response_data;
          this.result_color = res.data.result_color;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
        });
    },
    initForm() {
    },
    onSubmit(evt) {
      this.response_data = {
        is_email_valid: '',
        is_email_free: '',
        is_email_one_time: '',
        deliverability: '',
        mailgun: '',
      };
      evt.preventDefault();
      const payload = {
        email: this.addBookForm.email,
      };
      console.log(this.addBookForm.email);
      this.addBook(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.initForm();
    },
    editBook(book) {
      this.editForm = book;
    },
  },
  created() {
    // this.getBooks();
  },
};
</script>
