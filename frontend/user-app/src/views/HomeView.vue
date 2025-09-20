<template>
  <div class="home">
    <section class="hero">
      <h1>CampusGo 学生综合服务平台</h1>
      <p>一站式校园生活服务平台，为您提供拼车、二手交易和跑腿服务</p>
      <div class="hero-buttons">
        <router-link to="/trips" class="btn btn-primary">查找拼车</router-link>
        <router-link to="/secondhand" class="btn btn-primary">二手交易</router-link>
        <router-link to="/errands" class="btn btn-primary">跑腿服务</router-link>
        <router-link to="/register" class="btn btn-secondary">注册账户</router-link>
      </div>
    </section>

    <section class="features">
      <h2>为什么选择CampusGo？</h2>
      <div class="feature-grid">
        <div class="feature-card">
          <h3>多功能服务</h3>
          <p>拼车、二手交易、跑腿服务一站式解决</p>
        </div>
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

    <section class="services">
      <h2>我们的服务</h2>
      <div class="service-grid">
        <div class="service-card">
          <h3>拼车服务</h3>
          <p>轻松找到同行伙伴，安全便捷地共享出行</p>
          <router-link to="/trips" class="btn btn-small">立即体验</router-link>
        </div>
        <div class="service-card">
          <h3>二手交易</h3>
          <p>买卖学习用品、生活用品，环保又实惠</p>
          <router-link to="/secondhand" class="btn btn-small">立即体验</router-link>
        </div>
        <div class="service-card">
          <h3>跑腿服务</h3>
          <p>发布任务或接取任务，轻松赚取零花钱</p>
          <router-link to="/errands" class="btn btn-small">立即体验</router-link>
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
          <h3>选择服务</h3>
          <p>根据需求选择拼车、二手交易或跑腿服务</p>
        </div>
        <div class="step">
          <div class="step-number">3</div>
          <h3>发布或查找</h3>
          <p>发布您的需求或查找合适的服务</p>
        </div>
        <div class="step">
          <div class="step-number">4</div>
          <h3>完成交易</h3>
          <p>确认细节，愉快完成服务</p>
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
  width: 100%;
  max-width: 100%;
  margin: 0 auto;
  box-sizing: border-box;
}

.hero {
  text-align: center;
  padding: 2rem 1rem;
  background: linear-gradient(135deg, #42b883 0%, #42b883 100%);
  color: white;
  border-radius: 10px;
  margin-bottom: 2rem;
  width: 100%;
  box-sizing: border-box;
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
  box-sizing: border-box;
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

.btn-small {
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
  background-color: #42b883;
  color: white;
  border: none;
  display: inline-block;
  margin-top: 1rem;
  box-sizing: border-box;
}

.features {
  margin-bottom: 2rem;
  width: 100%;
  box-sizing: border-box;
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
  width: 100%;
  box-sizing: border-box;
}

.feature-card {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  width: 100%;
  box-sizing: border-box;
}

.feature-card h3 {
  margin-bottom: 1rem;
  color: #42b883;
  font-size: 1.2rem;
}

.services {
  margin-bottom: 2rem;
  width: 100%;
  box-sizing: border-box;
}

.services h2 {
  text-align: center;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
}

.service-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
  width: 100%;
  box-sizing: border-box;
}

.service-card {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  width: 100%;
  box-sizing: border-box;
}

.service-card h3 {
  margin-bottom: 1rem;
  color: #42b883;
  font-size: 1.2rem;
}

.how-it-works {
  margin-bottom: 2rem;
  width: 100%;
  box-sizing: border-box;
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
  width: 100%;
  box-sizing: border-box;
}

.step {
  text-align: center;
  width: 100%;
  box-sizing: border-box;
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

/* 响应式断点优化 */
/* 超小屏幕 (手机, 小于576px) */
@media (max-width: 575.98px) {
  .home {
    padding: 0.5rem 0;
  }
  
  .hero {
    padding: 1.5rem 0.75rem;
    margin-bottom: 1rem;
    border-radius: 8px;
  }
  
  .hero h1 {
    font-size: 1.5rem;
    margin-bottom: 0.75rem;
  }
  
  .hero p {
    font-size: 0.9rem;
    margin-bottom: 1rem;
  }
  
  .hero-buttons {
    gap: 0.75rem;
  }
  
  .btn {
    padding: 0.75rem;
    font-size: 0.9rem;
  }
  
  .features h2,
  .services h2,
  .how-it-works h2 {
    font-size: 1.25rem;
    margin-bottom: 1rem;
  }
  
  .feature-grid,
  .service-grid {
    gap: 0.75rem;
  }
  
  .feature-card,
  .service-card {
    padding: 1rem;
  }
  
  .feature-card h3,
  .service-card h3 {
    font-size: 1rem;
    margin-bottom: 0.75rem;
  }
  
  .feature-card p,
  .service-card p {
    font-size: 0.85rem;
  }
  
  .steps {
    gap: 1rem;
  }
  
  .step-number {
    width: 35px;
    height: 35px;
    font-size: 0.9rem;
  }
  
  .step h3 {
    font-size: 1rem;
    margin-bottom: 0.25rem;
  }
  
  .step p {
    font-size: 0.85rem;
  }
}

/* 小屏幕 (手机横屏, 576px及以上) */
@media (min-width: 576px) {
  .hero-buttons {
    flex-direction: row;
    justify-content: center;
    flex-wrap: wrap;
    gap: 0.75rem;
  }
  
  .btn {
    padding: 0.75rem 1.25rem;
    min-width: 120px;
  }
  
  .feature-grid,
  .service-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }
  
  .steps {
    grid-template-columns: repeat(2, 1fr);
    gap: 1.5rem;
  }
}

/* 中等屏幕 (平板, 768px及以上) */
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
    flex-wrap: wrap;
  }
  
  .btn {
    padding: 0.8rem 1.5rem;
    width: auto;
  }
  
  .feature-grid {
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
  }
  
  .service-grid {
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

/* 大屏幕 (桌面, 992px及以上) */
@media (min-width: 992px) {
  .hero {
    padding: 4rem 0;
  }
  
  .hero h1 {
    font-size: 2.8rem;
  }
  
  .hero p {
    font-size: 1.3rem;
    max-width: 800px;
    margin-left: auto;
    margin-right: auto;
  }
  
  .hero-buttons {
    gap: 1.5rem;
  }
  
  .btn {
    padding: 1rem 2rem;
    font-size: 1.1rem;
  }
  
  .feature-grid,
  .service-grid {
    gap: 2.5rem;
  }
  
  .feature-card,
  .service-card {
    padding: 2rem;
  }
  
  .steps {
    gap: 3rem;
  }
}

/* 超大屏幕 (大桌面, 1200px及以上) */
@media (min-width: 1200px) {
  .home {
    padding: 3rem 0;
    max-width: 1400px;
  }
  
  .hero {
    padding: 5rem 0;
    margin-bottom: 4rem;
  }
  
  .hero h1 {
    font-size: 3rem;
  }
  
  .hero p {
    font-size: 1.4rem;
  }
  
  .feature-grid,
  .service-grid {
    gap: 3rem;
  }
  
  .feature-card,
  .service-card {
    padding: 2.5rem;
  }
  
  .feature-card h3,
  .service-card h3 {
    font-size: 1.4rem;
  }
  
  .steps {
    gap: 4rem;
  }
  
  .step-number {
    width: 60px;
    height: 60px;
    font-size: 1.5rem;
  }
  
  .step h3 {
    font-size: 1.3rem;
  }
}

/* 超宽屏 (1600px及以上) */
@media (min-width: 1600px) {
  .home {
    padding: 4rem 0;
    max-width: 1600px;
  }
  
  .hero {
    padding: 6rem 0;
    margin-bottom: 5rem;
  }
  
  .hero h1 {
    font-size: 3.5rem;
  }
  
  .hero p {
    font-size: 1.6rem;
  }
  
  .btn {
    padding: 1.2rem 2.5rem;
    font-size: 1.3rem;
  }
  
  .feature-grid,
  .service-grid {
    gap: 4rem;
  }
  
  .feature-card,
  .service-card {
    padding: 3rem;
  }
  
  .feature-card h3,
  .service-card h3 {
    font-size: 1.6rem;
  }
  
  .steps {
    gap: 5rem;
  }
  
  .step-number {
    width: 70px;
    height: 70px;
    font-size: 1.8rem;
  }
  
  .step h3 {
    font-size: 1.5rem;
  }
}

/* 超宽屏 (2000px及以上) */
@media (min-width: 2000px) {
  .home {
    padding: 5rem 0;
    max-width: 1800px;
  }
  
  .hero {
    padding: 7rem 0;
    margin-bottom: 6rem;
  }
  
  .hero h1 {
    font-size: 4rem;
  }
  
  .hero p {
    font-size: 1.8rem;
  }
  
  .btn {
    padding: 1.5rem 3rem;
    font-size: 1.5rem;
  }
  
  .feature-grid,
  .service-grid {
    gap: 5rem;
  }
  
  .feature-card,
  .service-card {
    padding: 4rem;
  }
  
  .feature-card h3,
  .service-card h3 {
    font-size: 1.8rem;
  }
  
  .steps {
    gap: 6rem;
  }
  
  .step-number {
    width: 80px;
    height: 80px;
    font-size: 2rem;
  }
  
  .step h3 {
    font-size: 1.7rem;
  }
}
</style>