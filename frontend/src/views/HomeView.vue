<template>
  <div class="home">
    <section class="hero">
      <h1>UniGo 学生拼车平台</h1>
      <p>轻松找到同行伙伴，安全便捷地共享出行</p>
      <div class="hero-buttons">
        <router-link to="/trips" class="btn btn-primary">查找行程</router-link>
        <router-link to="/register" class="btn btn-secondary">注册账户</router-link>
      </div>
    </section>

    <section class="features">
      <h2>为什么选择UniGo？</h2>
      <div class="feature-grid">
        <div class="feature-card">
          <h3>安全可靠</h3>
          <p>实名认证，安全保障</p>
        </div>
        <div class="feature-card">
          <h3>便捷高效</h3>
          <p>一键发布，快速匹配</p>
        </div>
        <div class="feature-card">
          <h3>经济实惠</h3>
          <p>分摊费用，节省开支</p>
        </div>
      </div>
    </section>

    <section class="how-it-works">
      <h2>使用流程</h2>
      <div class="steps">
        <div class="step">
          <div class="step-number">1</div>
          <h3>注册账户</h3>
          <p>创建您的个人账户</p>
        </div>
        <div class="step">
          <div class="step-number">2</div>
          <h3>发布或查找行程</h3>
          <p>发布您的行程或查找合适的拼车</p>
        </div>
        <div class="step">
          <div class="step-number">3</div>
          <h3>确认预订</h3>
          <p>与同行伙伴确认细节</p>
        </div>
        <div class="step">
          <div class="step-number">4</div>
          <h3>愉快出行</h3>
          <p>准时出发，安全到达</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
// 组件逻辑可以在这里添加
</script>

<style scoped>
.home {
  padding: 1rem 0;
}

.hero {
  text-align: center;
  padding: 2rem 1rem;
  background: linear-gradient(135deg, #42b883 0%, #42b883 100%);
  color: white;
  border-radius: 10px;
  margin-bottom: 2rem;
}

.hero h1 {
  font-size: 2rem;
  margin-bottom: 1rem;
}

.hero p {
  font-size: 1rem;
  margin-bottom: 1.5rem;
}

.hero-buttons {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.btn {
  padding: 1rem;
  border-radius: 8px;
  text-decoration: none;
  font-weight: bold;
  transition: opacity 0.3s;
  text-align: center;
}

.btn:hover {
  opacity: 0.9;
}

.btn-primary {
  background-color: #fff;
  color: #42b883;
}

.btn-secondary {
  background-color: transparent;
  color: #fff;
  border: 2px solid #fff;
}

.features {
  margin-bottom: 2rem;
}

.features h2 {
  text-align: center;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
}

.feature-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

.feature-card {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.feature-card h3 {
  margin-bottom: 1rem;
  color: #42b883;
  font-size: 1.2rem;
}

.how-it-works {
  margin-bottom: 2rem;
}

.how-it-works h2 {
  text-align: center;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
}

.steps {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
}

.step {
  text-align: center;
}

.step-number {
  width: 40px;
  height: 40px;
  background-color: #42b883;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem;
  font-weight: bold;
  font-size: 1rem;
}

.step h3 {
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
}

/* 平板适配 */
@media (min-width: 768px) {
  .home {
    padding: 2rem 0;
  }
  
  .hero {
    padding: 3rem 0;
    margin-bottom: 3rem;
  }
  
  .hero h1 {
    font-size: 2.5rem;
  }
  
  .hero p {
    font-size: 1.2rem;
    margin-bottom: 2rem;
  }
  
  .hero-buttons {
    flex-direction: row;
    justify-content: center;
    gap: 1rem;
  }
  
  .btn {
    padding: 0.8rem 1.5rem;
    width: auto;
  }
  
  .feature-grid {
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
  }
  
  .steps {
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 2rem;
  }
  
  .step-number {
    width: 50px;
    height: 50px;
    font-size: 1.2rem;
  }
}
</style>