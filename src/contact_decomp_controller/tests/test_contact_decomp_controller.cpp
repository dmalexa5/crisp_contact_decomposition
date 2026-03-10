#include <gtest/gtest.h>
#include <stdexcept>

#include <contact_decomp_controller/contact_decomp_controller.hpp>

using crisp_controllers::ContactDecompController;

class TestContactDecompController : public ::testing::Test {
  public:
    static void SetUpTestSuite();
    static void TearDownTestSuite();

    void SetUp();
    void TearDown();

    void SetUpController();

    void SetUpControlLaw();

  protected:

    std::unique_ptr<ContactDecompController> controller_;
    std::shared_ptr<pinocchio::Model> model_;
    std::shared_ptr<pinocchio::Data> data_;

};

TEST(ContactDecompControllerTest, TestInitialization) {
    ASSERT_TRUE(true);
}
